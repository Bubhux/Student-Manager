import click
from rich.console import Console
from rich.table import Table

from controllers.student_controller import StudentDatabaseController


console = Console()

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
            table.add_row("2", "Ajouter un étudiant")
            table.add_row("3", "Ajouter une matière à un étudiant")
            table.add_row("4", "Modifier les notes d'un étudiant")
            table.add_row("5", "Modifier les informations d'un étudiant")
            table.add_row("6", "Calculer la moyenne d'un étudiant")
            table.add_row("7", "Supprimer un étudiant")
            table.add_row("r", "Retour au menu précedent")

            # Ajoute une chaîne vide avant le titre pour simuler l'alignement à gauche
            console.print()
            console.print("Menu gestion des étudiants", style="bold magenta")

            self.console.print(table)

            choice_menu = click.prompt(click.style("Choisissez le numéro de votre choix.", fg="green"), type=str)

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
        students = self.classroom_controller.get_all_students_database_controller()
        if not students:
            print("Il n'y a pas d'étudiants à afficher.")
        else:
            # Trie les étudiants par ordre alphabétique des noms et prénoms
            sorted_students = sorted(students, key=lambda x: (x['first_name']))

            print("Liste des étudiants triés par ordre alphabétique :")
            for index, student in enumerate(sorted_students, start=1):
                # Affiche le nom et prénom de l'étudiant
                student_name = f"{student['first_name']} {student['last_name']}"

                # Affiche le nom de la classe s'il est disponible
                classroom_name = student.get('classroom_name', 'N/A')

                # Si la classe est une liste, convertir en chaîne de caractères sans crochets
                if isinstance(classroom_name, list):
                    classroom_name = ', '.join(classroom_name)

                print(f"{index}. {student_name}, Classe : {classroom_name}")

        # Demande à l'utilisateur de saisir un étudiant par son nom, prénom ou ID
        self.display_student_informations(sorted_students) if students else None

    def display_student_informations(self, students):
        student_input = input("\nEntrez le nom, prénom ou le numéro de l'étudiant pour voir ses informations (ou 'r' pour revenir au menu précédent) :\n> ")

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
            print(f"Informations sur l'étudiant :")
            print(f"Nom : {selected_student['first_name']} {selected_student['last_name']}")
            print("Matières et notes :")
            for lesson in selected_student['lessons']:
                print(f"- {lesson['name']} : {lesson['grade']}")

            # Affiche la classe de l'étudiant sans les crochets si elle est une liste
            classroom_name = selected_student.get('classroom_name', 'N/A')
            if isinstance(classroom_name, list):
                classroom_name = ', '.join(classroom_name)
            
            print(f"Classe : {classroom_name}")
        else:
            print("Aucun étudiant trouvé avec cette entrée.")

    def add_student(self):
        first_name = input("Prénom de l'étudiant : ")
        last_name = input("Nom de l'étudiant (appuyez sur Entrée pour laisser vide) : ")

        # Demande le nombre de matières que cet étudiant suit
        while True:
            num_subjects_input = input("Combien de matières cet étudiant suit-il ? ")
            if num_subjects_input.isdigit() and int(num_subjects_input) > 0:
                num_subjects = int(num_subjects_input)
                break
            else:
                print("Veuillez saisir un nombre entier supérieur à 0.")

        subjects = []
        # Boucle pour saisir le nom et la note de chaque matière
        for i in range(num_subjects):
            subject_name = input(f"Nom de la matière {i+1}: ")
            while True:
                subject_grade_input = input(f"Note pour la matière {subject_name} (appuyez sur Entrée pour laisser la note à 0) : ")
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
            subjects.append({'name': subject_name, 'grade': subject_grade})

        # Crée une instance de StudentModel avec les données d'entrée
        student = StudentModel(first_name, last_name, lessons=subjects)

        # Valide les données d'entrée en appelant validate_input_data_student
        if student.validate_input_data_student():
            student_data = {
                'first_name': first_name,
                'last_name': last_name,
                'lessons': subjects,
                'grades': [subject['grade'] for subject in subjects]
            }
            self.classroom_controller.add_student_database_controller(student_data)
        else:
            print("Les données d'entrée sont invalides. Assurez-vous que toutes les notes sont comprises entre 0 et 20.")

    def add_subject_to_student(self):
        student_name = input("Nom de l'étudiant auquel vous souhaitez ajouter une matière (Prénom et Nom ou Prénom seul) : ")

        # Vérifie si l'étudiant existe
        student = self.classroom_controller.get_student_database_controller(student_name)
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
        self.classroom_controller.update_student_info_database_controller(student_name, student)
        print(f"Matière {subject_name} ajoutée à l'étudiant {student_name} avec la note {subject_grade}.")

    def update_student_grades(self):
        student_name = input("Nom de l'étudiant à modifier (Prénom et Nom ou Prénom seul) : ")

        # Vérifie si l'étudiant existe
        student = self.classroom_controller.get_student_database_controller(student_name)
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
            self.classroom_controller.update_student_grades_database_controller(student['first_name'], new_grades)

    def update_student_info(self):
        student_name = input("Nom de l'étudiant à mettre à jour (Prénom et Nom ou Prénom seul) : ")

        # Vérifie si l'étudiant existe
        student = self.classroom_controller.get_student_database_controller(student_name)
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
        self.classroom_controller.update_student_info_database_controller(student_name, new_student_data)

    def delete_student(self):
        student_name = input("Nom de l'étudiant à supprimer (Prénom et Nom ou Prénom seul) : ")
        self.classroom_controller.delete_student_database_controller(student_name)

    def calculate_student_average(self):
        student_name = input("Nom de l'étudiant à calculer la moyenne (Prénom et Nom ou Prénom seul) : ")
        average = self.classroom_controller.calculate_student_average_database_controller(student_name)
        if average is not None:
            print(f"Moyenne de {student_name} : {average:.2f}")
        else:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")

    def calculate_class_average(self):
        average = self.classroom_controller.calculate_class_average_database_controller()
        print(f"Moyenne de la classe : {average:.2f}")
