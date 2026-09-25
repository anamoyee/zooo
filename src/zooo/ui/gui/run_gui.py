import pathlib as p
import typing as t
import uuid

import dearpygui.dearpygui as dpg

from ... import api
from .dearpygui_glue import imgui_boilerplate


def spawn_pickle_warning_dialog(file_path: str):
	dialog_tag = f"pickle_warning_{uuid.uuid4()}"
	line1_tag = f"{dialog_tag}_line1"
	line2_tag = f"{dialog_tag}_line2"
	btn_group_tag = f"{dialog_tag}_btn_group"

	def update_layout():
		win_width = dpg.get_item_width(dialog_tag)
		assert win_width is not None
		if win_width <= 0:
			return

		line1_str = "using the import pickle feature may lead to arbitrary python code execution."
		line2_str = "make sure you trust the person who gave you the file to import"

		# Calculate pixel dimensions for text
		w1, _ = dpg.get_text_size(line1_str)
		w2, _ = dpg.get_text_size(line2_str)

		# Center text lines
		line1_item_indent = max(0.0, (win_width - w1) / 2)
		line2_item_indent = max(0.0, (win_width - w2) / 2)

		dpg.set_item_indent(line1_tag, int(line1_item_indent))
		dpg.set_item_indent(line2_tag, int(line2_item_indent))

		# Center button group (2 buttons of width 110 + 8px spacing = 228px total)
		btn_total_width = 110 + 110 + 8
		btn_item_indent = max(0.0, (win_width - btn_total_width) / 2)
		dpg.set_item_indent(btn_group_tag, int(btn_item_indent))

	def on_proceed():
		print(f"Successfully confirmed import for file: {file_path}")
		dpg.delete_item(dialog_tag)

	def on_cancel():
		dpg.delete_item(dialog_tag)

	with dpg.window(
		label="Security Warning",
		tag=dialog_tag,
		modal=False,
		no_collapse=True,
		width=650,
		height=240,
		min_size=(450, 200),
		pos=(150, 150),
	):
		dpg.add_spacer(height=10)

		# Dynamic text items
		dpg.add_text(
			"using the import pickle feature may lead to arbitrary python code execution.",
			tag=line1_tag,
		)
		dpg.add_text(
			"make sure you trust the person who gave you the file to import",
			tag=line2_tag,
		)

		dpg.add_spacer(height=25)

		# Centered Button Group
		with dpg.group(horizontal=True, tag=btn_group_tag):
			# Primary Styled Proceed Button
			btn_proceed = dpg.add_button(label="Proceed", width=110, callback=on_proceed)
			with dpg.theme() as proceed_theme, dpg.theme_component(dpg.mvButton):
				dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 119, 200, 255))
				dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (29, 140, 215, 255))
				dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 90, 160, 255))
			dpg.bind_item_theme(btn_proceed, proceed_theme)

			# Cancel Button
			dpg.add_button(label="Cancel", width=110, callback=on_cancel)

		# Attach item handler registry to capture window resize events
		with dpg.item_handler_registry() as handler_registry:
			dpg.add_item_resize_handler(callback=update_layout)
		dpg.bind_item_handler_registry(dialog_tag, handler_registry)

		# Perform initial alignment
		update_layout()


def file_selected_callback(sender: str, app_data: dict[str, t.Any]):
	selections = app_data.get("selections", {})
	if selections:
		file_path = next(iter(selections.values()))
	else:
		current_path = app_data.get("current_path", "")
		file_name = app_data.get("file_name", "")
		file_path = str(p.Path(current_path) / file_name)

	if file_path and p.Path(file_path).is_file():
		spawn_pickle_warning_dialog(file_path)


def run_gui(*zuhs: api.Zoo):
	with imgui_boilerplate():
		with dpg.file_dialog(
			directory_selector=False,
			show=False,
			callback=file_selected_callback,
			tag="pickle_file_dialog_id",
			width=700,
			height=400,
			label="Select Pickle File to Import",
		):
			# Green highlighted .pkl files without prefixes
			dpg.add_file_extension(".pkl", color=(0, 255, 0, 255))

			# Blue highlighted directories without prefixes
			# dpg.add_file_extension("", color=(100, 180, 255, 255), custom_text=" ")

			# Default white for all other files without prefixes
			dpg.add_file_extension(".*")

		# --- UI Setup ---
		with dpg.window(tag="Primary Window"):
			with dpg.menu_bar(), dpg.menu(label="Menu"):
				dpg.add_menu_item(label="New")
				dpg.add_menu_item(label="Open")
				dpg.add_menu_item(
					label="Import Pickle...",
					callback=lambda: dpg.show_item("pickle_file_dialog_id"),
				)
			dpg.add_text("Hello, Cross-Platform Dear PyGui!")
			dpg.add_button(label="Click Me")
