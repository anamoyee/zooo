#!/usr/bin/env -S uv run

# /// script
# dependencies = ["arguably", "rich"]
# ///

import pathlib as p
import re
import sys
from collections.abc import Callable
from types import CodeType
from typing import Any, NoReturn

import arguably
import rich
import rich.traceback

if True:  # Logging functions
	_log_console = rich.console.Console(highlight=False, file=sys.stderr)

	def log_success(msg: str) -> None:
		_log_console.print(f"[green bold]Success:[/] {msg}")

	def log_info(msg: str) -> None:
		_log_console.print(f"[blue bold]Info:[/] {msg}")

	def log_warning(msg: str) -> None:
		_log_console.print(f"[yellow bold]Warning:[/] {msg}")

	def log_error(msg: str) -> None:
		_log_console.print(f"[red bold]Error:[/] {msg}")

	def fatal(msg: str) -> NoReturn:
		log_error(msg)
		raise SystemExit(1)


@arguably.command
def __root__(
	path: p.Path,
	/,
	*,
	debug: bool = False,
	marker_regex_start: str = r"^\s*#\s*\[autosort(?:\((.*)\))?\]\s*$",
	marker_regex_end: str = r"^\s*#\s*\[/autosort\]\s*$",
	marker_regex_debug: str = r"\s*#\s?autosort_debug:.*",
):
	"""Automatically sort lines between designated comments in a file.

	Scans the given file for matching blocks wrapped by starting and ending comments,
	evaluates a sorting key for the contents inside each block, and writes the sorted
	results back to the file.

	Args:
		path: The path to the file whose blocks should be sorted.
		marker_regex_start: [-S] The regex used to match the starting comment line. Must support an optional custom Python evaluation expression enclosed in matching group 1.
		marker_regex_end: [-E] The regex used to match the ending comment line.
		marker_regex_debug: [-D] The regex used to match the debug comment line. Even if --debug is not present, all lines will be stripped of this regex before any run, then only if --debug is present new comments will be added, therefore not stacking debugs from previous runs, and being able to easily remove debug comments after done with them (just stop passing --debug and they will remove themselves automatically).
		debug: [-d] If True, appends an autosort debug comment to each line in the sorted blocks.
	"""
	if debug:
		log_info("Running in debug mode...")

	path = path.resolve()

	if not path.is_file():
		fatal(f"Path is not a file: {path}")

	try:
		start_re = re.compile(marker_regex_start)
		end_re = re.compile(marker_regex_end)
		debug_re = re.compile(marker_regex_debug)
	except re.error as e:
		fatal(f"Failed to compile marker regexes: {e}")

	try:
		lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
	except OSError as e:
		fatal(f"Failed to read file {path}: {e}")

	in_block = False
	start_line_idx = -1
	current_expr: str | None = None
	blocks_to_sort: list[tuple[int, int, str | None]] = []

	# 1. Validation and block discovery
	for i, line in enumerate(lines):
		start_match = start_re.match(line)
		end_match = end_re.match(line)

		if start_match:
			if in_block:
				fatal(
					f"Malformed markers in {path.name}: Found a start marker at line {i + 1}, "
					f"but already inside an open block from line {start_line_idx + 1}."
				)
			in_block = True
			start_line_idx = i
			current_expr = start_match.group(1)

		elif end_match:
			if not in_block:
				fatal(f"Malformed markers in {path.name}: Found an end marker at line {i + 1} without a preceding start marker.")
			in_block = False
			blocks_to_sort.append((start_line_idx, i, current_expr))
			current_expr = None

	if in_block:
		fatal(f"Malformed markers in {path.name}: Reached EOF but the block starting at line {start_line_idx + 1} was never closed.")

	if not blocks_to_sort:
		log_info(f"No autosort markers found in {path.name}.")
		return

	# 2. Sorting blocks in memory
	unchanged_count = 0

	def truelen(line: str) -> int:
		return len(line.split("#", maxsplit=1)[0].rstrip())

	for start_idx, end_idx, expr in blocks_to_sort:
		slice_start = start_idx + 1
		slice_end = end_idx

		if expr is not None:
			expr = expr.strip()

			# We have a custom python expression for this block
			try:
				# Compile ahead of the loop for better performance and early syntax error catching
				compiled_expr = compile(expr, "<string>", "eval")
			except SyntaxError as e:
				fatal(f"Syntax error in autosort expression {expr!r} at line {start_idx + 1}: {e}")

			# Use a factory function to bind the compiled expression in closure
			def make_custom_sort_key(compiled: CodeType, *, expr: str = expr, start_idx: int = start_idx) -> Callable[[str], Any]:
				def _key(line: str, *, expr: str = expr, start_idx: int = start_idx) -> Any:
					try:
						return (
							eval(
								compiled,
								globals(),
								{
									"_": line,
									"truelen": truelen,
								},
							),
							truelen(line),
						)
					except Exception as e:
						note_msg = (
							f"Error evaluating autosort expression {expr!r} on line {start_idx + 1}.\n"  #
							f"Evaluated line: {line.strip()!r}\nError: {e}"
						)
						e.add_note(note_msg)

				return _key

			sort_key: Callable[[str], Any] = make_custom_sort_key(compiled_expr)
		else:
			# Fallback to length of the line
			sort_key = truelen

		original_slice = lines[slice_start:slice_end]
		original_slice = [debug_re.sub("", original_line) for original_line in original_slice]

		sorted_slice = sorted(original_slice, key=sort_key)

		if original_slice == sorted_slice:
			unchanged_count += 1

		# remove debug comments from previous runs, even if --debug is not set

		if debug:
			longest_line_length = max(len(potential_longest_line.rstrip("\r\n")) for potential_longest_line in sorted_slice)

			def append_debug_comment(line: str, comment_text: str, *, longest_line_length: int = longest_line_length) -> str:
				line_endings = re.search(r"(\r\n|\r|\n)$", line)
				line_without_endings = line[: line_endings.start()] if line_endings else line

				padding = " " * (longest_line_length - len(line_without_endings))

				return f"{line_without_endings}{padding} # autosort_debug: {comment_text}{line_endings.group(0) if line_endings else ""}"

			sorted_slice = [
				append_debug_comment(sorted_line, str(sort_key(sorted_line)))  #
				for i, sorted_line in enumerate(sorted_slice, start=1)
			]

		lines[slice_start:slice_end] = sorted_slice

	# 3. Write back exactly once
	try:
		path.write_text("".join(lines), encoding="utf-8")

		total_blocks = len(blocks_to_sort)
		plural = "s" if total_blocks != 1 else ""

		if unchanged_count == 0:
			suffix = ""
		elif unchanged_count == total_blocks:
			suffix = f" (all {unchanged_count}/{total_blocks} unchanged)"
		else:
			suffix = f" ({unchanged_count}/{total_blocks} unchanged)"

		log_success(f"Sorted {total_blocks} block{plural} in {path.name}{suffix}")
	except OSError as e:
		fatal(f"Failed to write file {path}: {e}")


def main() -> int:
	rich.traceback.install()

	arguably.run()

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
