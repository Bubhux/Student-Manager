# views/main_menu_views.py
import click
from rich.console import Console
from rich.table import Table

from controllers.student_controller import StudentDatabaseController
from controllers.classroom_controller import ClassroomDatabaseController
from views.student_menu_views import StudentView
from views.classroom_menu_views import ClassroomView


class MainMenuView:

    def __init__(self, db):
        self.student_view = StudentView(db)
        self.classroom_view = ClassroomView(db)
        self.student_database_controller = StudentDatabaseController(db)
        self.classroom_database_controller = ClassroomDatabaseController(db)
        self.console = Console()

    def display_main_menu(self):

        while True:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Choix", style="cyan")
            table.add_column("Action", style="cyan")
            table.add_row("1", "Gestion des étudiants")
            table.add_row("2", "Gestion des classes")
            table.add_row("q", "Quitter le programme")

            # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
            self.console.print()
            self.console.print("Menu principal", style="bold magenta")

            self.console.print(table)

            choice_menu = click.prompt(
                click.style(
                    "Choisissez le numéro de votre choix \n>", fg="white"
                ),
                type=str,
                prompt_suffix=""
            )

            if choice_menu == "1":
                self.student_view.display_main_menu()
            elif choice_menu == "2":
                self.classroom_view.display_main_menu()
            elif choice_menu == "q":
                self.console.print("Merci d'avoir utilisé Student Manager !")
                break
            else:
                self.console.print(
                    "Choix invalide, saisissez un nombre entre 1 et 2 ou q pour quitter l'application.",
                    style="bold red"
                )
