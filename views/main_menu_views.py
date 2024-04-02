import click
from rich.console import Console
from rich.table import Table

from controllers.student_controller import StudentDatabaseController
from controllers.classroom_controller import ClassroomDatabaseController
from views.student_menu_views import StudentView
from views.classroom_menu_views import ClassroomView


console = Console()

class MainMenuView:

    def __init__(self):
        self.student_view = StudentView()
        self.classroom_view = ClassroomView()
        self.student_database_controller = StudentDatabaseController()
        self.classroom_database_controller = ClassroomDatabaseController()

    def display_main_menu(self):

        while True:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Choix")
            table.add_column("Action")
            table.add_row("1", "Gestion des étudiants", style="cyan")
            table.add_row("2", "Gestion des classes", style="cyan")
            table.add_row("3", "Quitter le programme", style="cyan")

            # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
            console.print()
            console.print(" Menu principal", style="bold magenta")

            console.print(table)

            choice_menu = click.prompt("Choisissez le numéro de votre choix.", type=int)

            if choice_menu == 1:
                self.student_view.display_main_menu()
            elif choice_menu == 2:
                self.classroom_view.display_main_menu()
            elif choice_menu == 3:
                console.print("Merci d'avoir utilisé ce programme !")
                break
            else:
                console.print("Choix invalide, saisissez un nombre entre 1 et 3.", style="bold red")
