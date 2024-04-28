import click
from rich.console import Console
from rich.table import Table

from controllers.classroom_controller import ClassroomDatabaseController
from controllers.student_controller import StudentDatabaseController

from models.classroom_models import ClassroomModel


class ClassroomView:

    def __init__(self):
        self.classroom_controller = ClassroomDatabaseController()
        self.student_controller = StudentDatabaseController()
        self.console = Console()

    def display_main_menu(self):

        while True:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Choix", style="cyan")
            table.add_column("Action", style="cyan")
            table.add_row("1", "Afficher les classes")
            table.add_row("2", "Créer une classe")
            table.add_row("3", "Modifier les informations d'une classe")
            table.add_row("4", "Ajouter des étudiants à une classe")
            table.add_row("5", "Supprimer des étudiants d'une classe")
            table.add_row("6", "Calculer la moyenne d'une classe")
            table.add_row("7", "Supprimer une classe")
            table.add_row("r", "Retour au menu précédent")

            # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
            self.console.print()
            self.console.print("Menu gestion des classes", style="bold magenta")
            self.console.print(table)

            choice_menu = click.prompt(click.style("Choisissez le numéro de votre choix ", fg="white"), type=str)

            if choice_menu == "1":
                self.display_classrooms()
            elif choice_menu == "2":
                self.add_classroom()
            elif choice_menu == "3":
                self.update_classroom_info()
            elif choice_menu == "4":
                self.add_students_to_classroom()
            elif choice_menu == "5":
                self.delete_students_from_classroom()
            elif choice_menu == "6":
                self.calculate_classroom_average()
            elif choice_menu == "7":
                self.delete_classroom()
            elif choice_menu == "r":
                self.console.print("Menu principal !")
                break
            else:
                self.console.print("Choix invalide, saisissez un nombre entre 1 et 6 ou r.", style="bold red")

    def display_classrooms(self):
        classrooms = self.classroom_controller.get_all_classrooms_database_controller()
        if not classrooms:
            self.console.print("Il n'y a pas de classes à afficher.")
        else:
            # Trie les classes par ordre alphabétique en fonction de leur nom
            sorted_classrooms = sorted(classrooms, key=lambda x: x['classroom_name'])

            # Crée un tableau pour afficher les classes
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Nom de la classe", style="cyan")
            table.add_column("Nombre de places disponibles", style="cyan")
            table.add_column("Nombre d'étudiants", style="cyan")

            for classroom in sorted_classrooms:
                # Vérifie le type de la valeur associée à 'number_of_students'
                if isinstance(classroom['number_of_students'], list):
                    num_students = len(classroom['number_of_students'])
                else:
                    num_students = classroom['number_of_students']

                # Ajoute une ligne au tableau avec les informations de la classe
                table.add_row(
                    classroom['classroom_name'],
                    str(classroom['number_of_places_available']),
                    str(num_students)
                )

            # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
            self.console.print()
            self.console.print("Liste des classes triées par ordre alphabétique", style="bold magenta")

            self.console.print(table)

    def add_students_to_classroom(self):

        while True:
            print("\nMenu gestion d'ajout d'étudiants")
            print("1. Afficher les classes disponibles")
            print("r. Retour au menu précédent")

            choice = input("Choisissez le numéro de votre choix.\n> ")

            if choice == "1":
                self.display_available_classes()
                break
            elif choice == "r":
                return
            else:
                print("Choix invalide, saisissez un 1 ou r.")

    def display_available_classes(self):

        while True:
            classrooms = self.classroom_controller.get_all_classrooms_database_controller()
            if not classrooms:
                print("Il n'y a pas de classes disponibles.")
            else:
                # Trie les classes par ordre alphabétique en fonction de leur nom
                sorted_classrooms = sorted(classrooms, key=lambda x: x['classroom_name'])

                print("Classes disponibles triés par ordre alphabétique :")
                for index, classroom in enumerate(sorted_classrooms, start=1):
                    print(f"{index}. {classroom['classroom_name']}")

                class_choice = input("Choisissez la classe à laquelle vous souhaitez ajouter des étudiants (ou 'r' pour revenir) :\n> ")
                if class_choice == "r":
                    return
                elif class_choice.isdigit():
                    class_choice = int(class_choice)
                    if 1 <= class_choice <= len(sorted_classrooms):
                        selected_class = sorted_classrooms[class_choice - 1]
                        self.add_students_to_selected_class(selected_class['classroom_name'])
                        break
                    else:
                        print("Choix invalide.")
                else:
                    print("Choix invalide, choisissez une classe disponible.")

    def add_students_to_selected_class(self, classroom_name):
        while True:
            num_students_to_add = input("Entrez le nombre d'étudiants à ajouter.\n> ")
            if num_students_to_add.isdigit():
                num_students_to_add = int(num_students_to_add)
                if num_students_to_add != 0:
                    break
                else:
                    print("Le nombre d'étudiants ne peut pas être 0.")
            else:
                print("Veuillez entrer un nombre valide.")

        # Récupére les étudiants déjà présents dans la classe sélectionnée
        current_students = self.classroom_controller.get_students_in_classroom_database_controller(classroom_name)

        # Affiche la liste des étudiants triés par ordre alphabétique
        students_from_database = self.student_controller.get_all_students_database_controller()
        if not students_from_database:
            print("Il n'y a pas d'élèves à afficher.")
            return

        sorted_students = sorted(students_from_database, key=lambda x: x['first_name'])

        print("Liste des étudiants triés par ordre alphabétique :")
        for index, student in enumerate(sorted_students, start=1):
            print(f"{index}. {student['first_name']} {student['last_name']}")

        # Liste pour stocker les étudiants sélectionnés
        selected_students = []
        for i in range(num_students_to_add):
            while True:
                student_choice = input(f"Saisissez le nom et prénom ou l'ID de l'étudiant {i+1} :\n> ")
                if student_choice.isdigit():
                    student_index = int(student_choice) - 1
                    if 0 <= student_index < len(sorted_students):
                        selected_student = sorted_students[student_index]
                        # Vérifie si l'étudiant est déjà dans une classe
                        if selected_student['_id'] in [student['_id'] for student in current_students]:
                            print(f"L'étudiant {selected_student['first_name']} {selected_student['last_name']} est déjà dans une classe.")
                        else:
                            selected_students.append(selected_student)
                            break
                    else:
                        print("ID invalide.")
                else:
                    try:
                        student_index = int(student_choice) - 1
                        if 0 <= student_index < len(sorted_students):
                            selected_student = sorted_students[student_index]
                            # Vérifie si l'étudiant est déjà dans une classe
                            if selected_student['_id'] in [student['_id'] for student in current_students]:
                                print(f"L'étudiant {selected_student['first_name']} {selected_student['last_name']} est déjà dans une classe.")
                            else:
                                selected_students.append(selected_student)
                                break
                        else:
                            print("ID invalide.")
                    except ValueError:
                        print("Nom/prénom invalide.")

        # Ajoute les étudiants sélectionnés à la classe
        self.classroom_controller.add_students_to_classroom_database_controller(classroom_name, selected_students)

    def delete_students_from_classroom(self):

        while True:
            print("\nMenu gestion de suppression d'étudiants")
            print("1. Afficher les classes disponibles")
            print("r. Retour au menu précédent")

            choice = input("Choisissez le numéro de votre choix.\n> ")

            if choice == "1":
                self.display_available_classes_for_deletion()
                break
            elif choice == "r":
                return
            else:
                print("Choix invalide, saisissez 1 ou r.")

    def display_available_classes_for_deletion(self):

        while True:
            classrooms = self.classroom_controller.get_all_classrooms_database_controller()
            if not classrooms:
                print("Il n'y a pas de classes disponibles.")
            else:
                # Trie les classes par ordre alphabétique en fonction de leur nom
                sorted_classrooms = sorted(classrooms, key=lambda x: x['classroom_name'])

                print("Classes disponibles triés par ordre alphabétique :")
                for index, classroom in enumerate(sorted_classrooms, start=1):
                    print(f"{index}. {classroom['classroom_name']}")

                class_choice = input("Choisissez la classe dont vous souhaitez supprimer des étudiants (ou 'r' pour revenir) :\n> ")
                if class_choice == "r":
                    return
                elif class_choice.isdigit():
                    class_choice = int(class_choice)
                    if 1 <= class_choice <= len(sorted_classrooms):
                        selected_class = sorted_classrooms[class_choice - 1]
                        self.remove_students_from_selected_class(selected_class['classroom_name'])
                        break
                    else:
                        print("Choix invalide.")
                else:
                    print("Choix invalide, choisissez une classe disponible.")

    def remove_students_from_selected_class(self, classroom_name):
        classroom = self.classroom_controller.get_classroom_database_controller(classroom_name)

        if not classroom:
            print(f"Aucune classe trouvée avec le nom {classroom_name}.")
            return

        students = classroom.get('number_of_students', [])
        if not students:
            print("Il n'y a pas d'étudiants dans cette classe à supprimer.")
            return

        # Trie les étudiants par ordre alphabétique en fonction de leur nom complet
        sorted_students = sorted(students, key=lambda x: (x['last_name'], x['first_name']))

        # Affiche la liste des étudiants dans la classe triée par ordre alphabétique
        print("Liste des étudiants dans la classe triés par ordre alphabétique :")
        for index, student in enumerate(sorted_students, start=1):
            print(f"{index}. {student['first_name']} {student['last_name']}")

        while True:
            num_students_to_remove = input("Entrez le nombre d'étudiants à supprimer.\n> ")
            if num_students_to_remove.isdigit():
                num_students_to_remove = int(num_students_to_remove)
                if num_students_to_remove != 0:
                    break
                else:
                    print("Le nombre d'étudiants à supprimer ne peut pas être 0.")
            else:
                print("Veuillez entrer un nombre valide.")

        for i in range(num_students_to_remove):
            while True:
                student_choice = input(f"Saisissez le numéro de l'étudiant {i+1} à supprimer :\n> ")
                if student_choice.isdigit():
                    student_index = int(student_choice) - 1
                    if 0 <= student_index < len(sorted_students):
                        student_to_remove = sorted_students.pop(student_index)
                        # Retire l'étudiant de sa classe actuelle
                        self.classroom_controller.remove_student_from_classroom_database_controller(classroom_name, student_to_remove)
                        # Met à jour le champ classroom_name dans le profil de l'étudiant
                        self.student_controller.remove_student_from_classroom(student_to_remove['_id'], classroom_name)
                        # print(f"{student_to_remove['first_name']} {student_to_remove['last_name']} supprimé de la classe {classroom_name}.")

                        # Affiche la liste des étudiants dans la classe triée par ordre alphabétique
                        print("Liste des étudiants dans la classe triés par ordre alphabétique :")
                        for index, student in enumerate(sorted_students, start=1):
                            print(f"{index}. {student['first_name']} {student['last_name']}")

                        break
                    else:
                        print("Numéro invalide.")
                else:
                    print("Veuillez entrer un numéro valide.")

        # Mise à jour du nombre d'étudiants dans la classe
        self.classroom_controller.update_classroom_info_database_controller(classroom_name, {'new_number_of_students': sorted_students})

    def add_classroom(self):
        classroom_name = input("Nom de la classe : ")
        number_of_places_available_input = input("Nombre de places disponibles (appuyez sur Entrée pour laisser vide) : ")
        number_of_students_input = input("Nombre d'étudiants (appuyez sur Entrée pour laisser vide) : ")

        # Vérifie si rien n'est saisi pour le nombre de places disponibles, puis définit 0 comme valeur par défaut
        if number_of_places_available_input:
            number_of_places_available = int(number_of_places_available_input)
        else:
            number_of_places_available = 0

        # Vérifie si rien n'est saisi pour le nombre d'étudiants, puis définit 0 comme valeur par défaut
        if number_of_students_input:
            number_of_students = int(number_of_students_input)
        else:
            number_of_students = 0

        # Crée une instance de ClassroomModel avec les données d'entrée
        new_classroom = ClassroomModel(
            classroom_name,
            number_of_places_available,
            number_of_students
        )

        # Valide les données d'entrée
        if new_classroom.validate_input_data_classroom():
            classroom_data = {
                'classroom_name': classroom_name,
                'number_of_places_available': number_of_places_available,
                'number_of_students': number_of_students
            }
            self.classroom_controller.add_classroom_database_controller(classroom_data)
            print("La classe a été ajoutée avec succès!")
        else:
            print("Les données d'entrée sont invalides.")

    def update_classroom_info(self):
        classroom_name = input("Nom de la classe à mettre à jour : ")

        # Vérifie si la classe existe
        classroom = self.classroom_controller.get_classroom_database_controller(classroom_name)
        if not classroom:
            print(f"Aucune classe trouvée avec le nom {classroom_name}. Vérifiez le nom de la classe.")
            return

        # Demande les nouvelles informations
        new_classroom_name = input("Nouveau nom de la classe (appuyez sur Entrée pour conserver le nom actuel) : ").strip()
        new_number_of_places_available = input("Nouveau nombre de places disponibles (appuyez sur Entrée pour conserver le nombre actuel) : ").strip()
        new_number_of_students = input("Nouveau nombre d'étudiants (appuyez sur Entrée pour laisser vide) : ").strip()

        # Vérifie si les nouvelles informations sont fournies, sinon conserve les informations actuelles
        new_classroom_name = new_classroom_name if new_classroom_name else classroom['classroom_name']
        new_number_of_places_available = new_number_of_places_available if new_number_of_places_available else classroom['number_of_places_available']
        new_number_of_students = new_number_of_students if new_number_of_students else classroom['number_of_students']

        # Crée un dictionnaire avec les nouvelles informations de la classe
        new_classroom_data = {
            'classroom_name': new_classroom_name,
            'new_number_of_places_available': new_number_of_places_available,
            'new_number_of_students': new_number_of_students
        }

        # Mettre à jour les informations de la classe
        self.classroom_controller.update_classroom_info_database_controller(classroom_name, new_classroom_data)

    def delete_classroom(self):
        classroom_name = input("Nom de la classe à supprimer. : ")
        self.classroom_controller.delete_classroom_database_controller(classroom_name)

    def calculate_classroom_average(self):
        classrooms = self.classroom_controller.get_all_classrooms_database_controller()

        if not classrooms:
            print("Il n'y a pas de classes disponibles.")
            return
        else:
            # Trie les classes par ordre alphabétique en fonction de leur nom
            sorted_classrooms = sorted(classrooms, key=lambda x: x['classroom_name'])

        print("Classes disponibles :")
        for index, classroom in enumerate(sorted_classrooms, start=1):
            print(f"{index}. Nom : {classroom['classroom_name']}")

        while True:
            choice = input("Choisissez le numéro de la classe pour calculer la moyenne (ou 'r' pour revenir) :\n> ")

            if choice == "r":
                return
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(sorted_classrooms):
                    selected_class = sorted_classrooms[choice - 1]
                    average = self.classroom_controller.calculate_classroom_average_database_controller(selected_class['classroom_name'])
                    if average is not None:
                        print(f"Moyenne de {selected_class['classroom_name']} : {average:.2f}")
                    else:
                        print(f"Aucune donnée trouvée pour la classe {selected_class['classroom_name']}. Vérifiez le nom de la classe.")
                    break
                else:
                    print("Choix invalide. Veuillez saisir un numéro valide.")
            else:
                print("Choix invalide, veuillez saisir un nombre ou 'r' pour revenir.")
