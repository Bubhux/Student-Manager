import click
from rich.console import Console
from rich.table import Table

from controllers.student_controller import StudentDatabaseController
from models.student_models import StudentModel


class StudentView:

    def __init__(self):
        self.student_controller = StudentDatabaseController()
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

            choice_menu = click.prompt(click.style("Choisissez le numéro de votre choix ", fg="white"), type=str)

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
            table.add_column("Nom et prénom", style="cyan")
            table.add_column("Classe", style="cyan")

            # Ajouter les étudiants au tableau
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
        student_input = click.prompt("\nEntrez le nom, prénom ou le numéro de l'étudiant pour voir ses informations (ou 'r' pour revenir au menu précédent) \n>", type=str, prompt_suffix="")

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
            # Recherche l'étudiant par son nom ou prénom
            for student in students:
                if student_input.lower() in student['first_name'].lower() or student_input.lower() in student['last_name'].lower():
                    selected_student = student
                    break

        # Affiche les informations de l'étudiant si trouvé, sinon afficher un message d'erreur
        if selected_student:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Attribut", style="cyan")
            table.add_column("Valeur", style="cyan")

            table.add_row("Nom", f"{selected_student['first_name']} {selected_student['last_name']}")

            # Construit une chaîne de caractères pour les matières et notes
            subjects_grades = "\n".join([f"- {lesson['name']} : {lesson['grade']}" for lesson in selected_student['lessons']])
            table.add_row("Matières et notes", subjects_grades)

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

            first_name = input("Prénom de l'étudiant : ").strip()
            if not first_name:
                self.console.print("Le prénom de l'étudiant ne peut pas être vide.", style="bold red")
                continue

            last_name = click.prompt("Nom de l'étudiant (appuyez sur Entrée pour laisser vide) ", type=str, default="", show_default=False)
            
            num_subjects_valid = False
            while not num_subjects_valid:
                num_subjects = input("Combien de matières cet étudiant suit-il ? (Appuyez sur Entrée pour ne choisir aucune matière) ")
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

        subjects = []
        for i in range(num_subjects):
            subject_name = click.prompt(f"Nom de la matière {i+1}", type=str)
            subject_grade = click.prompt(f"Note pour la matière {subject_name} (appuyez sur Entrée pour laisser la note à 0)", type=float, show_default=True)
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
        for subject in subjects:
            table.add_row(f"Matière : {subject['name']}", f"Note : {subject['grade']}")
        self.console.print(table)

        if click.confirm("Confirmez-vous l'ajout de cet étudiant ?", default=True, show_default=True):
            student_data = {
                'first_name': first_name,
                'last_name': last_name,
                'lessons': subjects,
                'grades': [subject['grade'] for subject in subjects]
            }
            self.student_controller.add_student_database_controller(student_data)
            self.console.print("[bold green]L'étudiant a été ajouté avec succès ![/bold green]")
        else:
            self.console.print("[bold red]L'ajout de l'étudiant a été annulé.[/bold red]")

    def add_subject_to_student(self):
        student_name = input("Nom de l'étudiant auquel vous souhaitez ajouter une matière (Prénom et Nom ou Prénom seul) : ")

        # Vérifie si l'étudiant existe
        student = self.student_controller.get_student_database_controller(student_name)
        if not student:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")
            return

        # Demande le nom de la nouvelle matière et la note
        subject_name = input("Nom de la nouvelle matière : ")
        while True:
            subject_grade_input = input("Note pour cette matière (appuyez sur Entrée pour laisser la note à 0) : ")
            if subject_grade_input.strip():
                try:
                    subject_grade = float(subject_grade_input)
                except ValueError:
                    print("Veuillez saisir un nombre valide pour la note.")
                    continue
                if 0 <= subject_grade <= 20:
                    break
                else:
                    print("La note doit être comprise entre 0 et 20.")
            else:
                subject_grade = 0.0
                break

        # Ajoute la nouvelle matière et note à la liste des matières de l'étudiant
        new_lesson = {'name': subject_name, 'grade': subject_grade}
        student['lessons'].append(new_lesson)

        # Met à jour les informations de l'étudiant dans la base de données
        self.student_controller.update_student_info_database_controller(student_name, student)
        print(f"Matière {subject_name} ajoutée à l'étudiant {student_name} avec la note {subject_grade}.")

    def update_student_grades(self):
        student_name = input("Nom de l'étudiant à modifier (Prénom et Nom ou Prénom seul) : ")

        # Vérifie si l'étudiant existe
        student = self.student_controller.get_student_database_controller(student_name)
        if not student:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")
            return

        # Demande les nouvelles notes
        new_grades = []
        for subject in student['lessons']:
            new_grade_input = input(f"Nouvelle note pour {subject['name']} (appuyez sur Entrée pour conserver la note actuelle) : ").strip()
            if new_grade_input:
                try:
                    new_grade = float(new_grade_input)
                except ValueError:
                    print("Veuillez saisir un nombre valide pour la note.")
                    return
                if not 0 <= new_grade <= 20:
                    print("La note doit être comprise entre 0 et 20.")
                    return
                new_grades.append({'name': subject['name'], 'grade': new_grade})
            else:
                new_grades.append({'name': subject['name'], 'grade': subject['grade']})

        # Valide les nouvelles notes
        updated_student = StudentModel(student['first_name'], student['last_name'], lessons=new_grades)
        if not updated_student.validate_input_data_student():
            print("Les nouvelles notes sont invalides. Assurez-vous que toutes les notes sont comprises entre 0 et 20.")
            return

        # Vérifie si les notes ont été modifiées
        unchanged = True
        for old_grade, new_grade in zip(student['lessons'], new_grades):
            if old_grade['grade'] != new_grade['grade']:
                unchanged = False
                break

        # Affiche les notes modifiées ou un message si elles n'ont pas été modifiées
        if unchanged:
            print("Aucune nouvelle note n'a été saisie. Les notes de l'étudiant restent inchangées :")
            for subject in student['lessons']:
                print(f"- Note de {subject['name']} : {subject['grade']}")
        else:
            print("Notes modifiées :")
            for new_grade in new_grades:
                print(f"- Nouvelle note de {new_grade['name']} : {new_grade['grade']}")

            # Mettre à jour les notes de l'étudiant en utilisant le nom de l'étudiant récupéré de la base de données
            self.student_controller.update_student_grades_database_controller(student['first_name'], new_grades)

    def update_student_info(self):
        student_name = input("Nom de l'étudiant à mettre à jour (Prénom et Nom ou Prénom seul) : ")

        # Vérifie si l'étudiant existe
        student = self.student_controller.get_student_database_controller(student_name)
        if not student:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")
            return

        # Demande les nouvelles informations
        new_first_name = input("Nouveau prénom (appuyez sur Entrée pour conserver le prénom actuel) : ").strip()
        new_last_name = input("Nouveau nom (appuyez sur Entrée pour conserver le nom actuel) : ").strip()
        new_classroom = input("Nouvelle classe (appuyez sur Entrée pour conserver la classe actuelle) : ").strip()

        # Vérifie si les nouvelles informations sont fournies, sinon conserve les informations actuelles
        new_first_name = new_first_name if new_first_name else student['first_name']
        new_last_name = new_last_name if new_last_name else student['last_name']
        new_classroom = new_classroom if new_classroom else student.get('classroom_name')

        # Liste pour stocker les nouvelles matières et notes de l'étudiant
        new_lessons = []

        # Boucle pour saisir les nouvelles matières et notes
        for lesson in student.get('lessons', []):
            lesson_name = input(f"Nouveau nom de la matière {lesson['name']} (appuyez sur Entrée pour conserver) : ").strip()
            if not lesson_name:
                lesson_name = lesson['name']

            lesson_grade_input = input(f"Nouvelle note pour la matière {lesson['name']} (appuyez sur Entrée pour conserver) : ").strip()
            if not lesson_grade_input:
                lesson_grade = lesson['grade']
            else:
                lesson_grade = float(lesson_grade_input)

            # Ajoute la matière et la note à la liste des nouvelles matières
            new_lessons.append({'name': lesson_name, 'grade': lesson_grade})

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

    def delete_student(self):
        student_name = input("Nom de l'étudiant à supprimer (Prénom et Nom ou Prénom seul) : ")
        self.student_controller.delete_student_database_controller(student_name)

    def calculate_student_average(self):
        student_name = input("Nom de l'étudiant à calculer la moyenne (Prénom et Nom ou Prénom seul) : ")
        average = self.student_controller.calculate_student_average_database_controller(student_name)
        if average is not None:
            print(f"Moyenne de {student_name} : {average:.2f}")
        else:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")

    def calculate_class_average(self):
        average = self.student_controller.calculate_class_average_database_controller()
        print(f"Moyenne de la classe : {average:.2f}")
