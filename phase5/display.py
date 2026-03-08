import logging
from typing import List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

logger = logging.getLogger(__name__)
console = Console()

class DisplayManager:
    
    def __init__(self, tagline: str = "Helping you find the best places to eat in bangalore city"):
        self.tagline = tagline

    def print_header(self):
       
        header_text = Text("\nZOMATO AI RECOMMENDER", style="bold magenta")
        header_text.append(f"\n{self.tagline}", style="italic cyan")
        
        console.print(Panel(
            header_text,
            title="[bold white]Phase 5: Final Display[/bold white]",
            border_style="bright_blue",
            expand=False
        ))

    def display_recommendations(self, recommendations: List[Any], city: str):
        
        if not recommendations:
            console.print(f"\n[bold yellow]No restaurants found in {city} matching your criteria.[/bold yellow]")
            return

        table = Table(title=f"\n[bold green]Top Recommendations in {city}[/bold green]", show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("Restaurant", style="bold cyan")
        table.add_column("Rating", justify="center")
        table.add_column("Cost (2)", justify="right")
        table.add_column("Cuisines")

        for i, rec in enumerate(recommendations, 1):
            rating_style = "green" if rec.rating >= 4.0 else "yellow" if rec.rating >= 3.0 else "red"
            table.add_row(
                str(i),
                rec.name,
                f"[{rating_style}]{rec.rating} ({rec.votes})[/{rating_style}]",
                f"₹{rec.average_cost}",
                rec.cuisines
            )

        console.print(table)
        

        console.print("\n[bold magenta] AI RECOMMENDATION REASONING:[/bold magenta]\n")
        for i, rec in enumerate(recommendations, 1):
            pass

    def print_ai_reasoning(self, name: str, reasoning: str):
        
        console.print(Panel(
            Text(reasoning),
            title=f"[bold cyan]{name}[/bold cyan]",
            border_style="green",
            padding=(1, 2)
        ))

    def print_footer(self):

        console.print("\n[dim]Thank you for using Zomato AI Recommender![/dim]")
        console.print("[dim]Helping you find the best places to eat in bangalore city[/dim]\n")
