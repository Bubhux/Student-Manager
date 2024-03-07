from controllers.student_controller import StudentDatabaseController
from controllers.classroom_controller import ClassroomDatabaseController

from views.student_menu_views import StudentView
from views.classroom_menu_views import ClassroomView


class MainMenuView:

    def __init__(self):
        self.student_view = StudentView()
        self.classroom_view = ClassroomView()
        self.student_database_controller = StudentDatabaseController()
        self.classroom_database_controller = ClassroomDatabaseController()

    def display_main_menu(self):

        while True:
            print("\nMenu principal")
            print("1. Gestion des étudiants")
            print("2. Gestion des classes")
            print("3. Quitter le programme\n")

            choice_menu = input("Choisissez le numéro de votre choix.\n> ")

            if choice_menu == "1":
                self.student_view.display_main_menu()

            elif choice_menu == "2":
                self.classroom_view.display_main_menu()

            elif choice_menu == "3":
                print("Merci d'avoir utilisé ce programme !")
                break
            else:
                print("Choix invalide, saisissez un nombre entre 1 et 3.")
