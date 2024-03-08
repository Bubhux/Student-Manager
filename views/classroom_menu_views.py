from controllers.classroom_controller import ClassroomDatabaseController
from controllers.student_controller import StudentDatabaseController
from models.classroom_models import ClassroomModel


class ClassroomView:

    def __init__(self):
        self.classroom_controller = ClassroomDatabaseController()
        self.student_controller = StudentDatabaseController()

    def display_main_menu(self):

        while True:
            print("\nMenu gestion des classes")
            print("1. Afficher les classes")
            print("2. Ajouter une classe")
            print("3. Modifier les informations d'une classe")
            print("4. Ajouter des étudiants à une classe")
            print("5. Calculer la moyenne d'une classe")
            print("6. Supprimer une classe")
            print("r. Retour au menu précédent")

            choice_menu = input("Choisissez le numéro de votre choix.\n> ")

            if choice_menu == "1":
                self.display_classrooms()
            elif choice_menu == "2":
                self.add_classroom()
            elif choice_menu == "3":
                self.update_classroom_info()
            elif choice_menu == "4":
                self.add_students_to_classroom()
            elif choice_menu == "5":
                self.update_student_info()
            elif choice_menu == "6":
                self.delete_classroom()
            elif choice_menu == "r":
                print("Menu principal !")
                break
            else:
                print("Choix invalide, saisissez un nombre entre 1 et 6 ou r.")

    def display_classrooms(self):
        classrooms = self.classroom_controller.get_all_classrooms_database_controller()
        if not classrooms:
            print("Il n'y a pas de classes à afficher.")
        else:
            print("Liste des classes :")
            for classroom in classrooms:
                # Vérifie le type de la valeur associée à 'number_of_students'
                if isinstance(classroom['number_of_students'], list):
                    num_students = len(classroom['number_of_students'])
                else:
                    num_students = classroom['number_of_students']

                # Affiche le nom de la classe et le nombre d'étudiants dans cette classe
                print(f"- {classroom['classroom_name']}, "
                    f"Nombre de places disponibles : {classroom['number_of_places_available']}, "
                    f"Nombre d'étudiants : {num_students}")

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
                print("Classes disponibles :")
                for index, classroom in enumerate(classrooms, start=1):
                    print(f"{index}. {classroom['classroom_name']}")

                class_choice = input("Choisissez la classe à laquelle vous souhaitez ajouter des étudiants (ou 'r' pour revenir) :\n> ")
                if class_choice == "r":
                    return
                elif class_choice.isdigit():
                    class_choice = int(class_choice)
                    if 1 <= class_choice <= len(classrooms):
                        selected_class = classrooms[class_choice - 1]
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
                        selected_students.append(sorted_students[student_index])
                        break
                    else:
                        print("ID invalide.")
                else:
                    try:
                        student_index = int(student_choice) - 1
                        if 0 <= student_index < len(sorted_students):
                            selected_students.append(sorted_students[student_index])
                            break
                        else:
                            print("ID invalide.")
                    except ValueError:
                        print("Nom/prénom invalide.")

        # Ajout des étudiants sélectionnés à la classe
        self.classroom_controller.add_students_to_classroom_database_controller(classroom_name, selected_students)

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

        # Créer une instance de ClassroomModel avec les données d'entrée
        new_classroom = ClassroomModel(
            classroom_name,
            number_of_places_available,
            number_of_students
        )

        # Valider les données d'entrée
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
            'new_number_of_students' : new_number_of_students
        }

        # Mettre à jour les informations de la classe
        self.classroom_controller.update_classroom_info_database_controller(classroom_name, new_classroom_data)

    def delete_classroom(self):
        classroom_name = input("Nom de la classe à supprimer. : ")
        self.classroom_controller.delete_classroom_database_controller(classroom_name)

    def calculate_classroom_average(self):
        classroom_name = input("Nom de la classe à calculer la moyenne. : ")
        average = self.classroom_controller.calculate_classroom_average_database_controller(classroom_name)
        if average is not None:
            print(f"Moyenne de {classroom_name} : {average:.2f}")
        else:
            print(f"Aucune classe trouvé avec le nom {classroom_name}. Vérifiez le nom de la classe.")
