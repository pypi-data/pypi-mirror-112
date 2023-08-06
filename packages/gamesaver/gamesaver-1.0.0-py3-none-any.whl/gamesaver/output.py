from rich import table
from rich.console import Console


class Table:
    def __init__(self, header_style: str, show_header: bool = True):
        self.console = Console()
        self.table = table.Table(header_style=header_style, show_header=show_header)
        self.table.add_column("Title")
        self.table.add_column("Store", style="cyan")
        self.table.add_column("Original Price", style="red")
        self.table.add_column("Sale Price", style="green")

    def print(self) -> None:
        self.console.print(self.table)
