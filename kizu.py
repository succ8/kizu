#!/bin/python

from textual import on
from rich.table import Table
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, OptionList, Input

LINES = open("anime.list")
ANIMES: tuple[tuple[str,int], ...] = (
    ("11 Eyes", "6751"),
    ("16 Bit", "17802")
)

class kizu(App):
    CSS_PATH = "layout.css"

    @staticmethod
    def anime(name: str, id: int) -> Table:
        table = Table(title=f"{name}", expand=True)
        table.add_column("Name")
        table.add_column("ID")
        table.add_row(name,id)
        return table

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Input(placeholder="Anime Name / ID")
        yield OptionList(*[self.anime(*row) for row in ANIMES])

    @on(OptionList.OptionSelected)
    def test(self) -> None:
        quit()

if __name__ == "__main__":
    app = kizu()
    app.run()
