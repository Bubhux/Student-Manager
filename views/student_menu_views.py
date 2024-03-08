from controllers.student_controller import StudentDatabaseController
from models.student_models import StudentModel


class StudentView:

    def __init__(self):
        self.database_controller = StudentDatabaseController()

    def display_main_menu(self):

        while True:
            print("\nMenu gestion des étudiants")
            print("1. Afficher les étudiants")
            print("2. Ajouter un étudiant")
            print("3. Modifier les notes d'un étudiant")
            print("4. Modifier les informations d'un étudiant")
            print("5. Calculer la moyenne d'un étudiant")
            print("6. Calculer la moyenne de la classe")
            print("7. Supprimer un étudiant")
            print("r. Retour au menu précedent\n")

            choice_menu = input("Choisissez le numéro de votre choix.\n> ")

            if choice_menu == "1":
                self.display_students()

            elif choice_menu == "2":
                self.add_student()

            elif choice_menu == "3":
                self.update_student_grades()

            elif choice_menu == "4":
                self.update_student_info()

            elif choice_menu == "5":
                self.calculate_student_average()

            elif choice_menu == "6":
                self.calculate_class_average()

            elif choice_menu == "7":
                self.delete_student()

            elif choice_menu == "r":
                print("Menu principal !")
                break
            else:
                print("Choix invalide, saisissez un nombre entre 1 et 7 ou r.")

    def display_students(self):
        students = self.database_controller.get_all_students_database_controller()
        if not students:
            print("Il n'y a pas d'étudiants à afficher.")
        else:
            print("Liste des étudiants :")
            for student in students:
                # Associe les matières aux notes, liste des matières pour lesquelles les notes sont enregistrées
                subjects = ['français ', 'mathématiques ', 'géographie ', 'histoire ']

                # Crée une liste de chaînes de caractères pour chaque matière et sa note associée
                # Explication de la compréhension de liste :
                #   - `zip(subjects, student['grades'])` combine les matières et les notes correspondantes en paires.
                #   - `for subject, grade in ...` parcourt chaque paire, où `subject` est la matière et `grade` est la note.
                #   - `f"{subject}: {grade}"` crée une chaîne de caractères au format "matière: note" pour chaque paire.
                grades_with_subjects = [f"{subject}: {grade}" for subject, grade in zip(subjects, student['grades'])]

                # Convertis la liste des notes et des matières en une seule chaîne de caractères séparée par des virgules
                # Explication de `join()` :
                #   - `join()` est une méthode de chaîne de caractères qui concatène les éléments d'une liste en une seule chaîne.
                #   - Ici, elle est utilisée pour fusionner les chaînes de caractères de chaque matière et sa note en une seule chaîne.
                grades_str = ', '.join(grades_with_subjects)
                print(f"- {student['first_name']} {student['last_name']}, Notes : {grades_str}")

    def add_student(self):
        first_name = input("Prénom de l'étudiant : ")
        last_name = input("Nom de l'étudiant (appuyez sur Entrée pour laisser vide) : ")
        french = input("Note de français (appuyez sur Entrée pour ignorer) : ")
        if french:
            french = float(french)

        math = input("Note de mathématiques (appuyez sur Entrée pour ignorer) : ")
        if math:
            math = float(math)

        geography = input("Note de géographie (appuyez sur Entrée pour ignorer) : ")
        if geography:
            geography = float(geography)

        history = input("Note d'histoire (appuyez sur Entrée pour ignorer) : ")
        if history:
            history = float(history)

        # Créer une instance de StudentModel avec les données d'entrée
        student = StudentModel(first_name, last_name, [french, math, geography, history])

        # Valide les données d'entrée en appelant validate_input_data_student
        if student.validate_input_data_student():
            student_data = {
                'first_name': first_name,
                'last_name': last_name,
                'grades': [french, math, geography, history]
            }
            self.database_controller.add_student_database_controller(student_data)
        else:
            print("Les données d'entrée sont invalides. Assurez-vous que toutes les notes sont comprises entre 0 et 20.")

    def update_student_grades(self):
        student_name = input("Nom de l'étudiant à modifier (Prénom et Nom ou Prénom seul) : ")
        
        # Vérifie si l'étudiant existe
        student = self.database_controller.get_student_database_controller(student_name)
        if not student:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")
            return

        # Demande les nouvelles notes
        french = input("Nouvelle note de français (appuyez sur Entrée pour conserver la note actuelle) : ").strip()
        math = input("Nouvelle note de mathématiques (appuyez sur Entrée pour conserver la note actuelle) : ").strip()
        geography = input("Nouvelle note de géographie (appuyez sur Entrée pour conserver la note actuelle) : ").strip()
        history = input("Nouvelle note d'histoire (appuyez sur Entrée pour conserver la note actuelle) : ").strip()

        # Convertis les notes en float s'ils sont fournis, sinon conserver les notes actuelles
        french = float(french) if french else student['grades'][0]
        math = float(math) if math else student['grades'][1]
        geography = float(geography) if geography else student['grades'][2]
        history = float(history) if history else student['grades'][3]

        # Créer une instance de StudentModel avec les nouvelles notes
        updated_student = StudentModel(student['first_name'], student['last_name'], [french, math, geography, history])

        # Valide les nouvelles notes en appelant validate_input_data_student
        if updated_student.validate_input_data_student():
            # Vérifie si les notes ont été modifiées
            new_grades = [french, math, geography, history]
            if new_grades == student['grades']:
                print("Aucune nouvelle note n'a été saisie. Les notes de l'étudiant restent inchangées :")
                print(f"- Note de français : {student['grades'][0]}")
                print(f"- Note de mathématiques : {student['grades'][1]}")
                print(f"- Note de géographie : {student['grades'][2]}")
                print(f"- Note d'histoire : {student['grades'][3]}")
            else:
                # Affiche les notes modifiées
                print("Notes modifiées :")
                if french != student['grades'][0]:
                    print(f"- Nouvelle note de français : {french}")
                if math != student['grades'][1]:
                    print(f"- Nouvelle note de mathématiques : {math}")
                if geography != student['grades'][2]:
                    print(f"- Nouvelle note de géographie : {geography}")
                if history != student['grades'][3]:
                    print(f"- Nouvelle note d'histoire : {history}")

                # Mettre à jour les notes de l'étudiant
                self.database_controller.update_student_grades_database_controller(student_name, new_grades)
        else:
            print("Les nouvelles notes sont invalides. Assurez-vous que toutes les notes sont comprises entre 0 et 20.")

    def update_student_info(self):
        student_name = input("Nom de l'étudiant à mettre à jour (Prénom et Nom ou Prénom seul) : ")

        # Vérifie si l'étudiant existe
        student = self.database_controller.get_student_database_controller(student_name)
        if not student:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")
            return

        # Demande les nouvelles informations
        new_first_name = input("Nouveau prénom (appuyez sur Entrée pour conserver le prénom actuel) : ").strip()
        new_last_name = input("Nouveau nom (appuyez sur Entrée pour conserver le nom actuel) : ").strip()

        # Vérifie si les nouvelles informations sont fournies, sinon conserve les informations actuelles
        new_first_name = new_first_name if new_first_name else student['first_name']
        new_last_name = new_last_name if new_last_name else student['last_name']

        # Crée un dictionnaire avec les nouvelles informations de l'étudiant
        new_student_data = {
            'first_name': new_first_name,
            'last_name': new_last_name,
            'grades': student['grades']  # Conserve les anciennes notes
        }

        # Mettre à jour les informations de l'étudiant
        self.database_controller.update_student_info_database_controller(student_name, new_student_data)

    def delete_student(self):
        student_name = input("Nom de l'étudiant à supprimer (Prénom et Nom ou Prénom seul) : ")
        self.database_controller.delete_student_database_controller(student_name)

    def calculate_student_average(self):
        student_name = input("Nom de l'étudiant à calculer la moyenne (Prénom et Nom ou Prénom seul) : ")
        average = self.database_controller.calculate_student_average_database_controller(student_name)
        if average is not None:
            print(f"Moyenne de {student_name} : {average:.2f}")
        else:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")

    def calculate_class_average(self):
        average = self.database_controller.calculate_class_average_database_controller()
        print(f"Moyenne de la classe : {average:.2f}")

