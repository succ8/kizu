#!/bin/python
import alist
from textual import on
from rich.table import Table
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer, OptionList, Input
from textual.widget import Widget

first_list = alist.gen_list()

class ListUpdate(Widget):
    anime_list = reactive([])

    @staticmethod
    def anime(id: str, name: str, eps: str, date: str) -> Table:
        table = Table(expand=True)
        table.add_column("Eps", width=5)
        table.add_column("Name", ratio=1)
        table.add_column("Air Date", width=10)
        table.add_row(eps,name,date)
        return table

    def get_list_as_tables(self):
        return [self.anime(*entry.values()) for entry in self.anime_list]
    
    #def on_mount(self):

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Anime Name / ID")
        self.anime_list = first_list.copy()
        yield OptionList(*self.get_list_as_tables())

    @on(Input.Changed)
    def show_new_list(self, event: Input.Changed) -> None:
        self.anime_list = alist.new_list(event.value, first_list)
        oplist = self.query_one(OptionList)
        oplist.clear_options()
        oplist.add_options(self.get_list_as_tables())

    @on(OptionList.OptionSelected)
    def test(self) -> None:
        quit()

class kizu(App):
    CSS_PATH = "layout.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ListUpdate()

if __name__ == "__main__":
    app = kizu()
    app.run()
