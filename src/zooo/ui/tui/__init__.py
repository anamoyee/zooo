import pathlib as p

from textual.app import App as BaseApp
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Collapsible, Digits, Label, TabbedContent, TabPane

from ... import api


class App(BaseApp):
	CSS = """
	Screen, VerticalScroll { align: center top; }
	Digits { width: auto; }
	"""

	BINDINGS = [
		Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
	]

	def __init__(
		self,
		*zuhs: api.Zoo,
		ids_file: p.Path,
		ansi_color: bool = False,
	):
		self.zuhs = zuhs

		super().__init__(
			ansi_color=ansi_color,
		)

	def on_mount(self):
		self.query_exactly_one(TabbedContent).active = "tab-2"

	def compose(self) -> ComposeResult:
		with TabbedContent():
			with TabPane("Data"):
				yield VerticalScroll(
					*(
						Collapsible(
							Label(zuh.name),
							title=f"Details for {zuh.name!r}",
							collapsed=True,
						)
						for zuh in self.zuhs
					),
				)

			with TabPane("Overview"):
				yield VerticalScroll(
					Collapsible(
						Label("Zooo 2"),
						title="Collapsible 2 title",
						collapsed=False,
					),
				)

			with TabPane("Leaderboard"):
				yield VerticalScroll(
					Collapsible(
						Label("Zooo 3"),
						title="Collapsible 3 title",
						collapsed=False,
					),
				)

			with TabPane("Utilities"):
				yield Vertical(
					Collapsible(
						Label("Zooo 4"),
						title="Collapsible 4 title",
						collapsed=False,
					),
					# bake IDs button
				)
