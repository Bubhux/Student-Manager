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
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Choix", style="cyan")
            table.add_column("Action", style="cyan")
            table.add_row("1", "Afficher les classes disponibles", style="cyan")
            table.add_row("r", "Retour au menu précédent", style="cyan")

            # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
            self.console.print()
            self.console.print("Menu gestion d'ajout d'étudiants", style="bold magenta")
            self.console.print(table)

            choice = click.prompt("Choisissez le numéro de votre choix", type=str)

            if choice == "1":
                self.display_available_classes()
                break
            elif choice.lower() == "r":
                return
            else:
                self.console.print("Choix invalide, saisissez 1 ou r.", style="bold red")

    def display_available_classes(self):

        while True:
            classrooms = self.classroom_controller.get_all_classrooms_database_controller()
            if not classrooms:
                self.console.print("Il n'y a pas de classes disponibles.", style="bold red")
            else:
                sorted_classrooms = sorted(classrooms, key=lambda x: x['classroom_name'])
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Numéro", style="cyan")
                table.add_column("Nom de la classe", style="cyan")
                for index, classroom in enumerate(sorted_classrooms, start=1):
                    table.add_row(str(index), classroom['classroom_name'])

                # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
                self.console.print()
                self.console.print("Classes disponibles triées par ordre alphabétique", style="bold magenta")
                self.console.print(table)

                class_choice = click.prompt("Choisissez la classe à laquelle vous souhaitez ajouter des étudiants (ou 'r' pour revenir)", type=str)
                if class_choice.lower() == "r":
                    return
                elif class_choice.isdigit():
                    class_choice = int(class_choice)
                    if 1 <= class_choice <= len(sorted_classrooms):
                        selected_class = sorted_classrooms[class_choice - 1]
                        self.add_students_to_selected_class(selected_class['classroom_name'])
                        break
                    else:
                        self.console.print("Choix invalide.", style="bold red")
                else:
                    self.console.print("Choix invalide, choisissez une classe disponible.", style="bold red")

    def add_students_to_selected_class(self, classroom_name):

        while True:
            num_students_to_add = click.prompt("Entrez le nombre d'étudiants à ajouter", type=int)
            if num_students_to_add != 0:
                break
            else:
                self.console.print("Le nombre d'étudiants ne peut pas être 0.", style="bold red")

        # Récupère les étudiants déjà présents dans la classe sélectionnée
        current_students = self.classroom_controller.get_students_in_classroom_database_controller(classroom_name)

        # Affiche la liste des étudiants triés par ordre alphabétique
        students_from_database = self.student_controller.get_all_students_database_controller()
        if not students_from_database:
            self.console.print("Il n'y a pas d'élèves à afficher.", style="bold red")
            return

        sorted_students = sorted(students_from_database, key=lambda x: x['first_name'])

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Numéro", style="cyan")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        for index, student in enumerate(sorted_students, start=1):
            table.add_row(str(index), student['last_name'], student['first_name'])

        # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
        self.console.print()
        self.console.print("Liste des étudiants triés par ordre alphabétique", style="bold magenta")
        self.console.print(table)

        # Liste pour stocker les étudiants sélectionnés
        selected_students = []
        for i in range(num_students_to_add):
            while True:
                student_choice = click.prompt(f"Saisissez le numéro de l'étudiant {i+1}", type=int)
                if 0 < student_choice <= len(sorted_students):
                    selected_student = sorted_students[student_choice - 1]
                    # Vérifie si l'étudiant est déjà dans une classe
                    if selected_student['_id'] in [student['_id'] for student in current_students]:
                        self.console.print(f"L'étudiant {selected_student['first_name']} {selected_student['last_name']} est déjà dans une classe.", style="bold red")
                    else:
                        selected_students.append(selected_student)
                        break
                else:
                    self.console.print("Numéro invalide, veuillez saisir un numéro valide.", style="bold red")

        # Ajoute les étudiants sélectionnés à la classe
        self.classroom_controller.add_students_to_classroom_database_controller(classroom_name, selected_students)

    def delete_students_from_classroom(self):

        while True:
            menu_table = Table(show_header=False, show_lines=False)
            menu_table.add_column("")
            menu_table.add_row("1. Afficher les classes disponibles", style="cyan")
            menu_table.add_row("r. Retour au menu précédent", style="cyan")

            self.console.print()
            self.console.print("Menu gestion de suppression d'étudiants", style="bold magenta")
            self.console.print(menu_table)

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
                self.console.print("Il n'y a pas de classes disponibles.")
            else:
                # Trie les classes par ordre alphabétique en fonction de leur nom
                sorted_classrooms = sorted(classrooms, key=lambda x: x['classroom_name'])

                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Numéro", justify="right", style="cyan")
                table.add_column("Nom de la classe", style="cyan")

                for index, classroom in enumerate(sorted_classrooms, start=1):
                    table.add_row(str(index), classroom['classroom_name'])

                self.console.print()
                self.console.print("Classes disponibles triés par ordre alphabétique", style="bold magenta")
                self.console.print(table)

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
                        self.console.print("Choix invalide.", style="red")
                else:
                    self.console.print("Choix invalide, choisissez une classe disponible.", style="red")

    def remove_students_from_selected_class(self, classroom_name):
        classroom = self.classroom_controller.get_classroom_database_controller(classroom_name)

        if not classroom:
            self.console.print(f"[bold red]Aucune classe trouvée avec le nom {classroom_name}.[/bold red]")
            return

        students = classroom.get('number_of_students', [])
        if not students:
            self.console.print("[bold yellow]Il n'y a pas d'étudiants dans cette classe à supprimer.[/bold yellow]")
            return

        # Trie les étudiants par ordre alphabétique en fonction de leur nom complet
        sorted_students = sorted(students, key=lambda x: (x['last_name'], x['first_name']))

        # Affiche la liste des étudiants dans la classe triée par ordre alphabétique
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Numéro", justify="right", style="cyan")
        table.add_column("Prénom", justify="left", style="cyan")
        table.add_column("Nom", justify="left", style="cyan")

        for index, student in enumerate(sorted_students, start=1):
            table.add_row(str(index), student['first_name'], student['last_name'])

        self.console.print()
        self.console.print("Liste des étudiants dans la classe triés par ordre alphabétique", style="bold magenta")
        self.console.print(table)

        while True:
            num_students_to_remove = input("Entrez le nombre d'étudiants à supprimer.\n> ")
            if num_students_to_remove.isdigit():
                num_students_to_remove = int(num_students_to_remove)
                if num_students_to_remove != 0:
                    break
                else:
                    self.console.print("[bold yellow]Le nombre d'étudiants à supprimer ne peut pas être 0.[/bold yellow]")
            else:
                self.console.print("[bold yellow]Veuillez entrer un nombre valide.[/bold yellow]")

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

                        # Met à jour la table
                        table = Table(show_header=True, header_style="bold magenta")
                        table.add_column("Numéro", justify="right", style="cyan")
                        table.add_column("Prénom", justify="left", style="cyan")
                        table.add_column("Nom", justify="left", style="cyan")
                        for index, student in enumerate(sorted_students, start=1):
                            table.add_row(str(index), student['first_name'], student['last_name'])

                        self.console.print()
                        self.console.print("Liste des étudiants dans la classe triés par ordre alphabétique", style="bold magenta")
                        self.console.print(table)

                        break
                    else:
                        self.console.print("[bold red]Numéro invalide.[/bold red]")
                else:
                    self.console.print("[bold red]Veuillez entrer un numéro valide.[/bold red]")

        # Mise à jour du nombre d'étudiants dans la classe
        self.classroom_controller.update_classroom_info_database_controller(classroom_name, {'new_number_of_students': sorted_students})

    def add_classroom(self):
        classroom_name = click.prompt("Nom de la classe : ")
        number_of_places_available_input = click.prompt("Nombre de places disponibles (appuyez sur Entrée pour laisser vide) ", type=str)
        number_of_students_input = click.prompt("Nombre d'étudiants (appuyez sur Entrée pour laisser vide) ", type=str)

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
            if click.confirm("Confirmez-vous la création de cette classe ?", default=True):
                self.classroom_controller.add_classroom_database_controller(classroom_data)
                self.console.print("[bold green]La classe a été ajoutée avec succès![/bold green]")
            else:
                self.console.print("[bold cyan]La création de la classe a été annulée.[/bold cyan]")
        else:
            self.console.print("[bold red]Les données d'entrée sont invalides.[/bold red]")

    def update_classroom_info(self):
        classroom_name = click.prompt("Nom de la classe à mettre à jour ", type=str)

        # Vérifie si la classe existe
        classroom = self.classroom_controller.get_classroom_database_controller(classroom_name)
        if not classroom:
            self.console.print(f"Aucune classe trouvée avec le nom [bold]{classroom_name}[/bold]. Vérifiez le nom de la classe.", style="bold red")
            return

        # Demande les nouvelles informations
        new_classroom_name = click.prompt("Nouveau nom de la classe (appuyez sur Entrée pour conserver le nom actuel) ", default=classroom['classroom_name'], type=str).strip()
        new_number_of_places_available = click.prompt("Nouveau nombre de places disponibles (appuyez sur Entrée pour conserver le nombre actuel) ", default=str(classroom['number_of_places_available']), type=int)
        new_number_of_students = click.prompt("Nouveau nombre d'étudiants (appuyez sur Entrée pour laisser vide) ", default=str(classroom['number_of_students']), type=int)

        # Vérifie si les nouvelles informations sont fournies, sinon conserve les informations actuelles
        new_classroom_name = new_classroom_name if new_classroom_name else classroom['classroom_name']
        new_number_of_places_available = new_number_of_places_available if new_number_of_places_available else classroom['number_of_places_available']
        new_number_of_students = new_number_of_students if new_number_of_students else classroom['number_of_students']

        # Crée un dictionnaire avec les nouvelles informations de la classe
        new_classroom_data = {
            'classroom_name': new_classroom_name,
            'number_of_places_available': new_number_of_places_available,
            'number_of_students': new_number_of_students
        }

        # Affiche les nouvelles informations de la classe dans un tableau
        table = Table(style="bold magenta")
        table.add_column("Champ")
        table.add_column("Valeur")

        table.add_row("Nom de la classe", new_classroom_name)
        table.add_row("Nombre de places disponibles", str(new_number_of_places_available))
        table.add_row("Nombre d'étudiants", new_number_of_students)

        # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
        self.console.print()
        self.console.print("Résumé des nouvelles informations de la classe", style="bold magenta")
        self.console.print(table)

        # Confirmation pour la mise à jour des informations
        if click.confirm("Confirmez-vous la mise à jour des informations de cette classe ?", default=True):
            self.classroom_controller.update_classroom_info_database_controller(classroom_name, new_classroom_data)
            self.console.print("[bold green]Les informations de la classe ont été mises à jour avec succès ![/bold green]")
        else:
            self.console.print("[bold cyan]La mise à jour des informations de la classe a été annulée.[/bold cyan]")

    def delete_classroom(self):
        classrooms = self.classroom_controller.get_all_classrooms_database_controller()

        if not classrooms:
            self.console.print("Il n'y a pas de classes disponibles.", style="bold red")
            return
        else:
            # Trie les classes par ordre alphabétique en fonction de leur nom
            sorted_classrooms = sorted(classrooms, key=lambda x: x['classroom_name'])

        # Affiche les classes disponibles dans un tableau
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Numéro", style="cyan")
        table.add_column("Nom de la classe", style="cyan")

        for index, classroom in enumerate(sorted_classrooms, start=1):
            table.add_row(str(index), classroom['classroom_name'])

        self.console.print()
        self.console.print("Classes disponibles pour suppression", style="bold magenta")
        self.console.print(table)

        while True:
            choice = click.prompt(click.style("Choisissez le numéro de la classe à supprimer (ou 'r' pour revenir) :", fg="white"), type=str, prompt_suffix="")

            if choice.lower() == "r":
                return
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(sorted_classrooms):
                    selected_class = sorted_classrooms[choice - 1]
                    confirm = click.confirm(click.style(f"Êtes-vous sûr de vouloir supprimer la classe '{selected_class['classroom_name']}' ?", fg="yellow"), default=False)
                    if confirm:
                        self.classroom_controller.delete_classroom_database_controller(selected_class['classroom_name'])
                        self.console.print(f"La classe '{selected_class['classroom_name']}' a été supprimée avec succès.", style="bold green")
                    else:
                        self.console.print("Suppression annulée.", style="bold red")
                    break
                else:
                    self.console.print("Choix invalide. Veuillez saisir un numéro valide.", style="bold red")
            else:
                self.console.print("Choix invalide, veuillez saisir un nombre ou 'r' pour revenir.", style="bold red")

    def calculate_classroom_average(self):
        classrooms = self.classroom_controller.get_all_classrooms_database_controller()

        if not classrooms:
            self.console.print("Il n'y a pas de classes disponibles.", style="bold red")
            return
        else:
            # Trie les classes par ordre alphabétique en fonction de leur nom
            sorted_classrooms = sorted(classrooms, key=lambda x: x['classroom_name'])

        # Affiche les classes disponibles dans un tableau
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Numéro", style="cyan")
        table.add_column("Nom de la classe", style="cyan")

        for index, classroom in enumerate(sorted_classrooms, start=1):
            table.add_row(str(index), classroom['classroom_name'])

        self.console.print()
        self.console.print("Classes disponibles triés par ordre alphabétique", style="bold magenta")
        self.console.print(table)

        while True:
            choice = click.prompt(click.style("Choisissez le numéro de la classe pour calculer la moyenne (ou 'r' pour revenir) :", fg="white"), type=str, prompt_suffix="")

            if choice == "r":
                return
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(sorted_classrooms):
                    selected_class = sorted_classrooms[choice - 1]
                    average = self.classroom_controller.calculate_classroom_average_database_controller(selected_class['classroom_name'])
                    if average is not None:
                        self.console.print(f"Moyenne de la classe de {selected_class['classroom_name']} : {average:.2f}", style="bold green")
                    else:
                        self.console.print(f"Aucune donnée trouvée pour la classe {selected_class['classroom_name']}. Vérifiez le nom de la classe.", style="bold red")
                    break
                else:
                    self.console.print("Choix invalide. Veuillez saisir un numéro valide.", style="bold red")
            else:
                self.console.print("Choix invalide, veuillez saisir un nombre ou 'r' pour revenir.", style="bold red")
