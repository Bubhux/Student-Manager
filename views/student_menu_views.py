# views/student_menu_views.py
import click
from rich.console import Console
from rich.table import Table

from controllers.student_controller import StudentDatabaseController
from controllers.classroom_controller import ClassroomDatabaseController

from models.student_models import StudentModel


class StudentView:

    def __init__(self, db):
        self.student_controller = StudentDatabaseController(db)
        self.classroom_controller = ClassroomDatabaseController(db)
        self.console = Console()

    def display_main_menu(self):

        while True:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Choix", style="cyan")
            table.add_column("Action", style="cyan")
            table.add_row("1", "Afficher les étudiants")
            table.add_row("2", "Créer un étudiant")
            table.add_row("3", "Ajouter une matière à un étudiant")
            table.add_row("4", "Modifier les notes d'un étudiant")
            table.add_row("5", "Modifier les informations d'un étudiant")
            table.add_row("6", "Calculer la moyenne d'un étudiant")
            table.add_row("7", "Supprimer un étudiant")
            table.add_row("r", "Retour au menu précedent")

            # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
            self.console.print()
            self.console.print("Menu gestion des étudiants", style="bold magenta")

            self.console.print(table)

            choice_menu = click.prompt(click.style("Choisissez le numéro de votre choix \n> ", fg="white"), type=str, prompt_suffix="")

            if choice_menu == "1":
                self.display_students()

            elif choice_menu == "2":
                self.add_student()

            elif choice_menu == "3":
                self.add_subject_to_student()

            elif choice_menu == "4":
                self.update_student_grades()

            elif choice_menu == "5":
                self.update_student_info()

            elif choice_menu == "6":
                self.calculate_student_average()

            elif choice_menu == "7":
                self.delete_student()

            elif choice_menu == "r":
                self.console.print("Menu principal !")
                break
            else:
                self.console.print("Choix invalide, saisissez un nombre entre 1 et 7 ou r.", style="bold red")

    def display_students(self):
        students = self.student_controller.get_all_students_database_controller()
        if not students:
            self.console.print("Il n'y a pas d'étudiants à afficher.", style="bold red")
        else:
            # Trie les étudiants par ordre alphabétique des noms et prénoms
            sorted_students = sorted(students, key=lambda x: (x['first_name']))

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Index", style="cyan")
            table.add_column("Prénom et nom", style="cyan")
            table.add_column("Classe", style="cyan")

            # Ajoute les étudiants au tableau
            for index, student in enumerate(sorted_students, start=1):
                student_name = f"{student['first_name']} {student['last_name']}"
                classroom_name = student.get('classroom_name', 'N/A')
                if isinstance(classroom_name, list):
                    classroom_name = ', '.join(classroom_name)
                table.add_row(str(index), student_name, classroom_name)

            self.console.print("Liste des étudiants triés par ordre alphabétique", style="bold magenta")
            self.console.print(table)

        # Demande à l'utilisateur de saisir un étudiant par son nom, prénom ou ID
        self.display_student_informations(sorted_students) if students else None

    def display_student_informations(self, students):
        student_input = click.prompt("\nEntrez le prénomn, nom ou le numéro de l'étudiant pour voir ses informations (Ou 'r' pour revenir au menu précédent) \n> ", type=str, prompt_suffix="")

        if student_input == 'r':
            return

        # Vérifie si l'entrée correspond à un nom, prénom ou numéro d'étudiant
        selected_student = None
        if student_input.isdigit():
            # Si l'entrée est un nombre, recherche l'étudiant par sa position dans la liste triée
            student_index = int(student_input) - 1  # Convertit en index de liste (commençant à 0)
            if 0 <= student_index < len(students):
                selected_student = students[student_index]
        else:
            # Sépare l'entrée de l'utilisateur en plusieurs parties (prénom et nom)
            student_input_parts = student_input.split()

            if len(student_input_parts) == 1:
                # Recherche par prénom ou nom si une seule partie est fournie
                for student in students:
                    if student_input_parts[0].lower() in student['first_name'].lower() or student_input_parts[0].lower() in student['last_name'].lower():
                        selected_student = student
                        break
            elif len(student_input_parts) == 2:
                # Recherche par combinaison prénom + nom
                first_name_input, last_name_input = student_input_parts
                for student in students:
                    if (first_name_input.lower() == student['first_name'].lower() and last_name_input.lower() == student['last_name'].lower()):
                        selected_student = student
                        break

        # Affiche les informations de l'étudiant si trouvé, sinon affiche un message d'erreur
        if selected_student:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Attribut", style="cyan")
            table.add_column("Valeur", style="cyan")

            table.add_row("Prénom et nom", f"{selected_student['first_name']} {selected_student['last_name']}")

            # Ajoute une ligne vide pour créer un espace
            table.add_row("", "")  # Ligne vide

            # Construit une chaîne de caractères pour les matières et notes
            subjects_grades = "\n".join([f"- {lesson['name']} : {lesson['grade']}" for lesson in selected_student['lessons']])
            table.add_row("Matières et notes", subjects_grades)

            # Ajoute une ligne vide pour créer un espace
            table.add_row("", "")  # Ligne vide

            classroom_name = selected_student.get('classroom_name', 'N/A')
            if isinstance(classroom_name, list):
                classroom_name = ', '.join(classroom_name)
            table.add_row("Classe", classroom_name)

            # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
            self.console.print()
            self.console.print("Informations sur l'étudiant", style="bold magenta")

            self.console.print(table)
        else:
            self.console.print("Aucun étudiant trouvé avec cette entrée.", style="bold red")

    def add_student(self):
        adding_student = True

        while adding_student:
            self.console.print("[bold cyan]Ajout d'un nouvel étudiant[/bold cyan]")

            first_name = input("Prénom de l'étudiant \n> ").strip()
            if not first_name:
                self.console.print("Le prénom de l'étudiant ne peut pas être vide.", style="bold red")
                continue

            last_name = click.prompt("Nom de l'étudiant (Appuyez sur Entrée pour laisser vide) \n> ", type=str, default="", show_default=False, prompt_suffix="")

            # Saisie facultative de la classe
            classroom_name = input("Nom de la classe (Appuyez sur Entrée pour ne pas ajouter l'étudiant à une classe) \n> ").strip()

            if classroom_name:
                classroom = ClassroomDatabaseController(self.student_controller.db).get_classroom_database_controller(classroom_name)
                if not classroom:
                    self.console.print(f"[bold red]La classe '{classroom_name}' n'existe pas.[/bold red]")
                    continue

                if classroom["number_of_places_available"] <= classroom.get("number_of_students", 0):
                    self.console.print(f"[bold red]La classe '{classroom_name}' n'a plus de places disponibles.[/bold red]")
                    continue

            # Saisie du nombre de matières
            num_subjects_valid = False
            while not num_subjects_valid:
                num_subjects = input("Combien de matières cet étudiant suit-il ? (Appuyez sur Entrée pour ne choisir aucune matière) \n> ")
                if num_subjects.strip() == "":
                    num_subjects = 0
                    num_subjects_valid = True
                else:
                    try:
                        num_subjects = int(num_subjects)
                        if num_subjects < 0:
                            self.console.print("Veuillez saisir un nombre entier supérieur ou égal à 0.", style="bold red")
                        else:
                            num_subjects_valid = True
                    except ValueError:
                        self.console.print("Veuillez saisir un nombre entier supérieur ou égal à 0.", style="bold red")

            # Si le prénom n'est pas vide et le nombre de matières est valide, sortir de la boucle
            adding_student = False

        # Saisie des matières et notes
        subjects = []
        for i in range(num_subjects):
            subject_name = click.prompt(f"Nom de la matière {i+1} \n> ", type=str, prompt_suffix="")
            subject_grade = click.prompt(f"Note pour la matière {subject_name} (appuyez sur Entrée pour laisser la note à 0) \n> ", type=float, default=0, show_default=False, prompt_suffix="")
            if not (0 <= subject_grade <= 20):
                self.console.print("La note doit être comprise entre 0 et 20.", style="bold red")
                return
            subjects.append({'name': subject_name, 'grade': subject_grade})

        self.console.print("[bold cyan]Résumé des informations saisies :[/bold cyan]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Attribut", style="cyan")
        table.add_column("Valeur", style="cyan")
        table.add_row("Prénom", first_name)
        table.add_row("Nom", last_name if last_name else "Non renseigné")
        if classroom_name:
            table.add_row("Classe", classroom_name)
        for subject in subjects:
            table.add_row(f"Matière : {subject['name']}", f"Note : {subject['grade']}")
        self.console.print(table)

        if click.confirm("Confirmez-vous l'ajout de cet étudiant ?", default=True, show_default=True):
            # Création de l'étudiant
            student_data = {
                'first_name': first_name,
                'last_name': last_name,
                'lessons': subjects,
                'grades': [subject['grade'] for subject in subjects]
            }

            if classroom_name:
                student_data['classroom_name'] = classroom_name

                # Ajoute l'étudiant à la liste des étudiants de la classe
                try:
                    # Récupère les étudiants existants dans la classe
                    number_of_students = classroom.get("number_of_students", [])
                    
                    if isinstance(number_of_students, list):
                        # Ajoute le nouvel étudiant à la liste
                        updated_students = number_of_students + [student_data]
                    elif isinstance(number_of_students, int):
                        # Si c'est un nombre, le convertir en liste
                        updated_students = [student_data]
                    else:
                        raise ValueError("Type inattendu pour 'number_of_students' dans la base de données.")
                    
                    # Mettre à jour la base de données pour la classe
                    ClassroomDatabaseController(self.student_controller.db).update_classroom_info_database_controller(
                        classroom_name, {'number_of_students': updated_students}
                    )
                except Exception as e:
                    print(f"Une erreur s'est produite lors de l'ajout de l'étudiant à la classe {classroom_name} : {str(e)}")

            # Ajoute l'étudiant à la base de données des étudiants
            self.student_controller.add_student_database_controller(student_data)
            self.console.print("[bold green]L'étudiant a été ajouté avec succès ![/bold green]")
        else:
            self.console.print("[bold red]L'ajout de l'étudiant a été annulé.[/bold red]")

    def add_subject_to_student(self):
        student_name = click.prompt("Nom de l'étudiant auquel vous souhaitez ajouter une matière (Prénom et Nom ou Prénom seul)", type=str)

        # Vérifie si l'étudiant existe
        student = self.student_controller.get_student_database_controller(student_name)
        if not student:
            self.console.print(f"Aucun étudiant trouvé avec le nom [bold]{student_name}[/bold]. Vérifiez le nom de l'étudiant.", style="bold red")
            return

        # Demande le nom de la nouvelle matière et la note
        subject_name = click.prompt("Nom de la nouvelle matière", type=str)
        while True:
            subject_grade_input = click.prompt("Note pour cette matière (appuyez sur Entrée pour laisser la note à 0)", default="", type=str, show_default=False)
            if subject_grade_input.strip():
                try:
                    subject_grade = float(subject_grade_input)
                    if not (0 <= subject_grade <= 20):
                        self.console.print("La note doit être comprise entre 0 et 20.", style="bold red")
                        continue
                    break
                except ValueError:
                    self.console.print("Veuillez saisir un nombre valide pour la note.", style="bold red")
            else:
                subject_grade = 0.0
                break

        # Affiche un résumé des informations saisies
        self.console.print("[bold cyan]Résumé des informations saisies :[/bold cyan]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Attribut", style="cyan")
        table.add_column("Valeur", style="cyan")
        table.add_row("Étudiant", student_name)
        table.add_row("Matière", subject_name)
        table.add_row("Note", str(subject_grade))
        self.console.print(table)

        # Demande de confirmation pour l'ajout de la matière
        confirmation = click.confirm("Confirmez-vous l'ajout de cette matière ?", default=True, show_default=True)
        if confirmation:
            # Ajoute la nouvelle matière et note à la liste des matières de l'étudiant
            new_lesson = {'name': subject_name, 'grade': subject_grade}
            student['lessons'].append(new_lesson)

            # Met à jour les informations de l'étudiant dans la base de données
            self.student_controller.update_student_info_database_controller(student_name, student)
            self.console.print(f"Matière [bold]{subject_name}[/bold] ajoutée à l'étudiant [bold]{student_name}[/bold] avec la note [bold]{subject_grade}[/bold].", style="bold green")
        else:
            self.console.print("[bold cyan]L'ajout de la matière a été annulé.[/bold cyan]")

    def update_student_grades(self):
        student_name = click.prompt("Nom de l'étudiant à modifier (Prénom et Nom ou Prénom seul) ", type=str)

        # Vérifie si l'étudiant existe
        student = self.student_controller.get_student_database_controller(student_name)
        if not student:
            self.console.print(f"Aucun étudiant trouvé avec le nom [bold]{student_name}[/bold]. Vérifiez le nom de l'étudiant.", style="bold red")
            return

        # Demande les nouvelles notes
        new_grades = []
        for subject in student['lessons']:
            new_grade_input = click.prompt(f"Nouvelle note pour {subject['name']} (appuyez sur Entrée pour conserver la note actuelle)", default=str(subject['grade']), type=str, prompt_suffix=" : ").strip()
            if new_grade_input:
                try:
                    new_grade = float(new_grade_input)
                except ValueError:
                    self.console.print("Veuillez saisir un nombre valide pour la note.", style="bold red")
                    return
                if not 0 <= new_grade <= 20:
                    self.console.print("La note doit être comprise entre 0 et 20.", style="bold red")
                    return
            else:
                new_grade = subject['grade']
            new_grades.append({'name': subject['name'], 'grade': new_grade})

        # Valide les nouvelles notes
        updated_student = StudentModel(student['first_name'], student['last_name'], lessons=new_grades)
        if not updated_student.validate_input_data_student():
            self.console.print("Les nouvelles notes sont invalides. Assurez-vous que toutes les notes sont comprises entre 0 et 20.", style="bold red")
            return

        # Vérifie si les notes ont été modifiées
        unchanged = all(old_grade['grade'] == new_grade['grade'] for old_grade, new_grade in zip(student['lessons'], new_grades))

        # Affiche les notes modifiées ou un message si elles n'ont pas été modifiées
        if unchanged:
            self.console.print("Aucune nouvelle note n'a été saisie. Les notes de l'étudiant restent inchangées :", style="bold blue")
            for subject in student['lessons']:
                self.console.print(f"- Note de {subject['name']} : {subject['grade']}")
        else:
            self.console.print("Notes modifiées :", style="bold blue")
            for new_grade in new_grades:
                self.console.print(f"- Nouvelle note de {new_grade['name']} : {new_grade['grade']}")

            # Mettre à jour les notes de l'étudiant en utilisant le nom de l'étudiant récupéré de la base de données
            if click.confirm("Confirmez-vous la mise à jour des notes de cet étudiant ?", default=True):
                self.student_controller.update_student_grades_database_controller(student['first_name'], new_grades)
                self.console.print("Les notes de l'étudiant ont été mises à jour avec succès !", style="bold green")
            else:
                self.console.print("La mise à jour des notes de l'étudiant a été annulée.", style="bold cyan")

    def update_student_info(self):
        student_name = click.prompt("Nom de l'étudiant à mettre à jour (Prénom et Nom ou Prénom seul) ", type=str)

        # Vérifie si l'étudiant existe
        student = self.student_controller.get_student_database_controller(student_name)
        if not student:
            self.console.print(f"Aucun étudiant trouvé avec le nom [bold]{student_name}[/bold]. Vérifiez le nom de l'étudiant.", style="bold red")
            return

        # Demande les nouvelles informations
        new_first_name = click.prompt(f"Nouveau prénom (appuyez sur Entrée pour conserver le prénom actuel) [{student['first_name']}] : ", default="", type=str, show_default=False, prompt_suffix="")
        if not new_first_name:
            new_first_name = student['first_name']

        new_last_name = click.prompt(f"Nouveau nom (appuyez sur Entrée pour conserver le nom actuel) [{student['last_name']}] : ", default="", type=str, show_default=False, prompt_suffix="")
        if not new_last_name:
            new_last_name = student['last_name']

        new_classroom = click.prompt(f"Nouvelle classe (appuyez sur Entrée pour conserver la classe actuelle) ", type=str, show_default=False, default="").strip()

        # Vérifie si la classe saisie existe et a des places disponibles
        if new_classroom:
            classroom = ClassroomDatabaseController(self.student_controller.db).get_classroom_database_controller(new_classroom)
            if not classroom:
                self.console.print(f"La classe [bold]{new_classroom}[/bold] n'existe pas. Vérifiez le nom de la classe.", style="bold red")
                return
            if classroom.get('number_of_places_available', 0) <= 0:
                self.console.print(f"La classe [bold]{new_classroom}[/bold] n'a plus de places disponibles.", style="bold red")
                return
        else:
            new_classroom = student.get('classroom_name', None)

        # Liste pour stocker les nouvelles matières et notes de l'étudiant
        new_lessons = []

        # Boucle pour saisir les nouvelles matières et notes
        for lesson in student.get('lessons', []):
            lesson_name = click.prompt(f"Nouveau nom de la matière {lesson['name']} (appuyez sur Entrée pour conserver) [{lesson['name']}] :", default=lesson['name'], type=str, show_default=False, prompt_suffix="")
            lesson_grade_input = input(f"Nouvelle note pour la matière {lesson['name']} (appuyez sur Entrée pour conserver) [{lesson['grade']}] : ").strip()

            # Si aucun nouveau nom n'est saisi, conserve le nom actuel
            if not lesson_name:
                lesson_name = lesson['name']

            # Si aucune nouvelle note n'est saisie, conserve la note actuelle
            if not lesson_grade_input:
                lesson_grade = lesson['grade']
            else:
                try:
                    lesson_grade = float(lesson_grade_input)
                except ValueError:
                    self.console.print("Veuillez saisir un nombre valide pour la note.", style="bold red")
                    return

            # Ajoute la matière et la note à la liste des nouvelles matières
            new_lessons.append({'name': lesson_name, 'grade': lesson_grade})

        # Affiche les nouvelles informations de l'étudiant dans un tableau
        table = Table(style="bold magenta")
        table.add_column("Champ")
        table.add_column("Valeur")

        table.add_row("Prénom", new_first_name)
        table.add_row("Nom", new_last_name)
        table.add_row("Classe", new_classroom)

        for lesson in new_lessons:
            table.add_row(f"Matière: {lesson['name']}", f"Note: {lesson['grade']}")

        # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
        self.console.print()
        self.console.print("Résumé des nouvelles informations de l'étudiant", style="bold magenta")

        self.console.print(table)

        # Confirmation pour la mise à jour des informations
        if click.confirm("Confirmez-vous la mise à jour des informations de cet étudiant ?", default=True):
            # Crée un dictionnaire avec les nouvelles informations de l'étudiant
            new_student_data = {
                'first_name': new_first_name,
                'last_name': new_last_name,
                'grades': student['grades'],  # Conserve les anciennes notes
                'classroom_name': new_classroom,
                'lessons': new_lessons
            }

            # Mettre à jour les informations de l'étudiant
            self.student_controller.update_student_info_database_controller(student_name, new_student_data)
            
            # Met à jour la classe de l'étudiant dans la base de données des classes
            self.classroom_controller.add_students_to_classroom_database_controller(new_classroom, [student])
            self.console.print("[bold green]Les informations de l'étudiant ont été mises à jour avec succès ![/bold green]")
        else:
            self.console.print("[bold red]La mise à jour des informations de l'étudiant a été annulée.[/bold red]")

    def delete_student(self):
        # Récupére tous les étudiants de la base de données
        students = self.student_controller.get_all_students_database_controller()

        # Vérifie s'il n'y a pas d'étudiants
        if not students:
            self.console.print("Il n'y a pas d'étudiants disponibles.", style="bold red")
            return
        else:
            # Trie les étudiants par ordre alphabétique en fonction de leur prénom
            sorted_students = sorted(students, key=lambda x: (x['first_name']))

        # Affiche les étudiants disponibles dans un tableau
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Numéro", style="cyan")
        table.add_column("Nom et prénom", style="cyan")
        table.add_column("Classe", style="cyan")

        # Remplis le tableau avec les informations des étudiants
        for index, student in enumerate(sorted_students, start=1):
            student_name = f"{student['first_name']} {student['last_name']}"
            classroom_name = student.get('classroom_name', 'N/A')
            if isinstance(classroom_name, list):
                classroom_name = ', '.join(classroom_name)
            table.add_row(str(index), student_name, classroom_name)

        # Imprime la liste triée des étudiants
        self.console.print()
        self.console.print("Liste des étudiants triés par ordre alphabétique", style="bold magenta")
        self.console.print(table)

        while True:
            # Demande à l'utilisateur de choisir un numéro d'étudiant ou de revenir
            choice = click.prompt(click.style("Choisissez le numéro de l'étudiant à supprimer (ou 'r' pour revenir) :", fg="white"), type=str, prompt_suffix="")

            if choice.lower() == "r":
                return
            elif choice.isdigit():
                choice = int(choice)
                # Vérifie si le choix est dans la plage valide
                if 1 <= choice <= len(sorted_students):
                    selected_student = sorted_students[choice - 1]
                    # Crée le nom complet de l'étudiant
                    student_name = f"{selected_student['first_name']} {selected_student['last_name']}"
                    # Demande confirmation avant la suppression
                    confirm = click.confirm(click.style(f"Êtes-vous sûr de vouloir supprimer l'étudiant '{student_name}' ?", fg="yellow"), default=False)
                    if confirm:
                        self.student_controller.delete_student_database_controller(student_name)
                    else:
                        self.console.print("Suppression annulée.", style="bold red")
                    break
                else:
                    self.console.print("Choix invalide. Veuillez saisir un numéro valide.", style="bold red")
            else:
                self.console.print("Choix invalide, veuillez saisir un nombre ou 'r' pour revenir.", style="bold red")

    def calculate_student_average(self):
        # Récupére tous les étudiants de la base de données
        students = self.student_controller.get_all_students_database_controller()

        # Vérifie s'il n'y a pas d'étudiants
        if not students:
            self.console.print("Il n'y a pas d'étudiants disponibles.", style="bold red")
            return
        else:
            # Trie les étudiants par ordre alphabétique en fonction de leur prénom
            sorted_students = sorted(students, key=lambda x: (x['first_name']))

        # Affiche les étudiants disponibles dans un tableau
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Numéro", style="cyan")
        table.add_column("Nom et prénom", style="cyan")
        table.add_column("Classe", style="cyan")

        # Remplir le tableau avec les informations des étudiants
        for index, student in enumerate(sorted_students, start=1):
            student_name = f"{student['first_name']} {student['last_name']}"
            classroom_name = student.get('classroom_name', 'N/A')
            if isinstance(classroom_name, list):
                classroom_name = ', '.join(classroom_name)
            table.add_row(str(index), student_name, classroom_name)

        # Imprime la liste triée des étudiants
        self.console.print()
        self.console.print("Liste des étudiants triés par ordre alphabétique", style="bold magenta")
        self.console.print(table)

        while True:
            # Demande à l'utilisateur de choisir un numéro d'étudiant ou de revenir
            choice = click.prompt(click.style("Choisissez le numéro de l'étudiant pour calculer la moyenne (ou 'r' pour revenir) :", fg="white"), type=str, prompt_suffix="")

            if choice == "r":
                return
            elif choice.isdigit():
                choice = int(choice)
                # Vérifie si le choix est dans la plage valide
                if 1 <= choice <= len(sorted_students):
                    selected_student = sorted_students[choice - 1]
                    # Combine le prénom et le nom pour correspondre aux enregistrements de la base de données
                    student_full_name = f"{selected_student['first_name']} {selected_student['last_name']}"
                    # Calcul la moyenne de l'étudiant
                    average = self.student_controller.calculate_student_average_database_controller(student_full_name)
                    if average is not None:
                        self.console.print(f"Moyenne de l'étudiant {student_full_name} : {average:.2f}", style="bold green")
                    else:
                        self.console.print(f"Aucune donnée trouvée pour l'étudiant {student_full_name}. Vérifiez le nom de l'étudiant.", style="bold red")
                    break
                else:
                    self.console.print("Choix invalide. Veuillez saisir un numéro valide.", style="bold red")
            else:
                self.console.print("Choix invalide, veuillez saisir un nombre ou 'r' pour revenir.", style="bold red")

    def calculate_class_average(self):
        average = self.student_controller.calculate_class_average_database_controller()
        print(f"Moyenne de la classe : {average:.2f}")
