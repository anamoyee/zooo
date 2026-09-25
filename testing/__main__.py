import asyncio

import rich.markup

from .resources import AsyncFn0, install_rich_traceback


def get_test_fns() -> list[AsyncFn0[None]]:
	from . import (
		client_lp,
		client_zoo,
	)

	return [
		client_zoo.client_zoo,
		client_lp.client_lp,
	]


def print_header(title: str) -> None:
	main_line = f"[yellow b]### [white b]{rich.markup.escape(title)}[/] ###[/]"
	side_line = "[yellow b]" + "#" * len(rich.markup.render(main_line).plain) + "[/]"

	rich.print(
		f"""

{side_line}
{main_line}
{side_line}

"""[1:-1]
	)


async def main() -> None:
	install_rich_traceback()

	for fn in get_test_fns():
		print_header(fn.__name__)

		await fn()


if __name__ == "__main__":
	asyncio.run(main())
