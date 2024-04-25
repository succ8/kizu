#!/bin/python
import alist
from textual import on
from rich.table import Table
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, OptionList, Input

animeList: list[list[str, str, str, str], ...] = alist.gen_list()

class kizu(App):
    CSS_PATH = "layout.css"

    @staticmethod
    def anime(id: str, name: str, eps: str, date: str) -> Table:
        table = Table(expand=True)
        table.add_column("Eps", width=5)
        table.add_column("Name", ratio=1)
        table.add_column("Air Date", width=10)
        table.add_row(eps,name,date)
        return table

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Input(placeholder="Anime Name / ID")
        yield OptionList(*[self.anime(*entry.values()) for entry in animeList])

    @on(OptionList.OptionSelected)
    def test(self) -> None:
        quit()

if __name__ == "__main__":
    app = kizu()
    app.run()
