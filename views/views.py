from controllers.database_controller import DatabaseController


class StudentView:

    def __init__(self):
        self.database_controller = DatabaseController()

    def display_students(self):
        students = self.database_controller.get_all_students()
        if not students:
            print("Il n'y a pas d'élèves à afficher.")
        else:
            print("Liste des élèves :")
            for student in students:
                print(f"- {student['first_name']} {student['last_name']}, Notes : {student['grades']}")

    def calculate_and_display_student_average(self, student_name, average):
        if average is not None:
            print(f"Moyenne de {student_name} : {average:.2f}")
        else:
            print(f"{student_name} n'est pas dans la liste")

    def calculate_and_display_class_average(self, average):
        if average is not None:
            print(f"Moyenne de la classe : {average:.2f}")
        else:
            print("Il n'y a pas d'élèves dans la classe.")

class MainMenuView:

    def __init__(self):
        self.student_view = StudentView()
        self.database_controller = DatabaseController()

    def display_main_menu(self):

        while True:
            print("\nMenu principal")
            print("1. Afficher les élèves")
            print("2. Ajouter un élève")
            print("3. Modifier les notes d'un élève")
            print("4. Calculer la moyenne d'un élève")
            print("5. Calculer la moyenne de la classe")
            print("6. Supprimer un élève")
            print("7. Quitter le programme\n")

            choice_menu = input("Choisissez le numéro de votre choix : ")

            if choice_menu == "1":
                self.student_view.display_students()

            elif choice_menu == "2":
                self.add_student()

            elif choice_menu == "3":
                self.update_student_grades()

            elif choice_menu == "4":
                self.calculate_student_average()

            elif choice_menu == "5":
                self.calculate_class_average()

            elif choice_menu == "6":
                self.delete_student()

            elif choice_menu == "7":
                print("Merci d'avoir utilisé ce programme !")
                break
            else:
                print("Choix invalide, saisissez un nombre entre 1 et 7.")

    def add_student(self):
        first_name = input("Prénom de l'élève : ")
        last_name = input("Nom de l'élève (appuyez sur Entrée pour laisser vide) : ")
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

        student_data = {
            'first_name': first_name,
            'last_name': last_name,
            'grades': [french, math, geography, history]
        }
        self.database_controller.add_student(student_data)

    def update_student_grades(self):
        student_name = input("Nom de l'élève à modifier (Prénom et Nom ou Prénom seul) : ")
        
        # Vérifie si l'étudiant existe
        student = self.database_controller.get_student(student_name)
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

        # Vérifie si les notes ont été modifiées
        new_grades = [french, math, geography, history]
        if new_grades == student['grades']:
            print("Aucune nouvelle note n'a été saisie. Les notes de l'étudiant restent inchangées :")
            print(f"- Note de français : {student['grades'][0]}")
            print(f"- Note de mathématiques : {student['grades'][1]}")
            print(f"- Note de géographie : {student['grades'][2]}")
            print(f"- Note d'histoire : {student['grades'][3]}")
        else:
            # Afficher les notes modifiées
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
            self.database_controller.update_student_grades(student_name, new_grades)

    def calculate_student_average(self):
        student_name = input("Nom de l'élève à calculer la moyenne (Prénom et Nom ou Prénom seul) : ")
        average = self.database_controller.calculate_student_average(student_name)
        print(f"Moyenne de {student_name} : {average:.2f}")

    def calculate_class_average(self):
        average = self.database_controller.calculate_class_average()
        print(f"Moyenne de la classe : {average:.2f}")

    def delete_student(self):
        student_name = input("Nom de l'élève à supprimer (Prénom et Nom ou Prénom seul) : ")
        self.database_controller.delete_student(student_name)
