import abc

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class Notification(abc.ABC):
    @abc.abstractmethod
    def print(self, name: str, current_version: str, latest_version: str) -> None:
        ...


class Poetry(Notification):
    def print(self, name: str, current_version: str, latest_version: str) -> None:
        console = Console()
        console.print(
            Align.center(
                Panel.fit(
                    Text.from_markup(
                        f"Update available [dim]{current_version}[/dim] → [green]{latest_version}[/green]"
                        f"\n"
                        f"Run [cyan]poetry update {name}[/cyan] to update",
                        justify="center",
                    ),
                    border_style="yellow",
                ),
            ),
        )
