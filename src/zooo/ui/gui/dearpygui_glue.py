import contextlib
import platform
from pathlib import Path

import dearpygui.dearpygui as dpg


def find_system_font() -> str | None:
	font_path_candidates = {
		"Linux": [
			"/usr/share/fonts/TTF/DejaVuSans.ttf",
			"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
			"/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
			"/usr/share/fonts/noto/NotoSans-Regular.ttf",
		],
		"Windows": [
			"C:\\Windows\\Fonts\\segoeui.ttf",
			"C:\\Windows\\Fonts\\arial.ttf",
		],
		"Darwin": [
			"/System/Library/Fonts/SFNS.ttf",
			"/Library/Fonts/Arial.ttf",
			"/System/Library/Fonts/Supplemental/Arial.ttf",
		],
	}.get(platform.system(), [])

	for font_path in font_path_candidates:
		if Path(font_path).is_file():
			return font_path

	return None


@contextlib.contextmanager
def imgui_boilerplate():
	dpg.create_context()

	font = find_system_font()

	print(f"{font=!r}")

	with dpg.font_registry():
		if font:
			app_font = dpg.add_font(font, 18)
			dpg.bind_font(app_font)

	try:
		yield
	finally:
		dpg.create_viewport(title="My Application", width=800, height=600)
		dpg.setup_dearpygui()
		dpg.set_primary_window("Primary Window", True)

		dpg.show_viewport()
		dpg.start_dearpygui()
		dpg.destroy_context()
