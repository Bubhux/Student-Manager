# controllers/classroom_controller.py
from models.student_models import StudentModel
from models.classroom_models import ClassroomModel

from bson import ObjectId


class ClassroomDatabaseController:

    def __init__(self, db):
        self.db = db
        self.student_collection = self.db['students']
        self.classroom_collection = self.db['classrooms']

    def connect_to_database(self):
        try:
            # Vérifie la connexion à la base de données
            self.db.command("ping")
            print(
                f"Connexion de ClassroomDatabaseController à la base de données MongoDB "
                f"'{self.db.name}' établie avec succès."
            )
        except Exception as e:
            print("ClassroomDatabaseController erreur de connexion à la base de données MongoDB :", str(e))
            raise

    def add_classroom_database_controller(self, classroom_data):
        existing_classroom = self.classroom_collection.find_one({'classroom_name': classroom_data['classroom_name']})
        if existing_classroom:
            print(
                f"Une classe avec le nom {classroom_data['classroom_name']} existe déjà. "
                "Impossible d'ajouter la classe."
            )
        else:
            try:
                self.classroom_collection.insert_one(classroom_data)
                print(f"La classe {classroom_data['classroom_name']} a été ajoutée avec succès!")
            except Exception as e:
                print(f"Une erreur s'est produite lors de l'ajout de la classe : {str(e)}")

    def get_classroom_database_controller(self, classroom_name):
        if isinstance(classroom_name, list):
            classroom_name = classroom_name[0]  # Obtient le premier élément de la liste
        return self.classroom_collection.find_one({'classroom_name': classroom_name})

    def get_all_classrooms_database_controller(self):
        classrooms = list(self.classroom_collection.find())
        if not classrooms:
            return []
        return classrooms

    def get_classroom_by_student_id(self, student_id):
        # Parcourt toutes les classes pour vérifier si l'étudiant est déjà inscrit
        all_classrooms = self.get_all_classrooms_database_controller()
        for classroom in all_classrooms:
            student_ids = classroom.get('number_of_students', [])
            if isinstance(student_ids[0], dict):
                student_ids = [student['_id'] for student in student_ids]
            if ObjectId(student_id) in map(ObjectId, student_ids):
                return classroom['classroom_name']
        return None

    def get_students_in_classroom_database_controller(self, classroom_name):
        # Récupère les informations de la classe depuis la base de données
        classroom_info = self.classroom_collection.find_one({'classroom_name': classroom_name})

        if classroom_info:
            # Récupère les IDs des étudiants dans la classe, en vérifiant si c'est une liste
            student_ids = classroom_info.get('number_of_students', [])

            if isinstance(student_ids, int):
                student_ids = [student_ids]

            # Assurez-vous que student_ids contient bien des ObjectId
            if isinstance(student_ids[0], dict):
                student_ids = [student['_id'] for student in student_ids]

            # Récupère les informations complètes des étudiants à partir de leur ID
            students_info = []
            for student_id in student_ids:
                student = self.student_collection.find_one({'_id': ObjectId(student_id)})
                if student:
                    students_info.append(student)

            return students_info
        else:
            print(f"Aucune classe trouvée avec le nom {classroom_name}.")
            return []

    def update_classroom_info_database_controller(self, classroom_name, new_classroom_data):
        # Recherche de la classe par son nom
        classroom = self.classroom_collection.find_one({'classroom_name': classroom_name})

        if classroom:
            try:
                # Création d'une instance de ClassroomModel avec les nouvelles données
                updated_classroom = ClassroomModel(
                    new_classroom_data.get('classroom_name', classroom['classroom_name']),
                    new_classroom_data.get('number_of_places_available', classroom['number_of_places_available']),
                    new_classroom_data.get('number_of_students', classroom['number_of_students'])
                )

                # Mise à jour des données de la classe dans la base de données
                self.classroom_collection.update_one({'_id': classroom['_id']}, {'$set': {
                    'classroom_name': updated_classroom.classroom_name,
                    'number_of_places_available': updated_classroom.number_of_places_available,
                    'number_of_students': updated_classroom.number_of_students
                }})

                print(f"Les informations de la classe {classroom_name} ont été mises à jour avec succès !")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la mise à jour des informations de la classe : {str(e)}")
        else:
            print(f"Aucune classe trouvée avec le nom {classroom_name}. Vérifiez le nom de la classe.")

    def add_students_to_classroom_database_controller(self, classroom_name, students):
        classroom = self.get_classroom_database_controller(classroom_name)
        if classroom:
            try:
                # Assure que number_of_students est une liste
                number_of_students = (
                    classroom["number_of_students"]
                    if isinstance(classroom["number_of_students"], list)
                    else []
                )

                # Nombre de places disponibles
                available_places = classroom['number_of_places_available']

                # Mettre à jour la classe de chaque étudiant ajouté
                for student in students:
                    student_id = student['_id']
                    student_info = self.student_collection.find_one({'_id': student_id})

                    if student_info:
                        # Assure que classroom_name est une liste
                        student_classroom = student_info.get('classroom_name', [])
                        if not isinstance(student_classroom, list):
                            student_classroom = []  # Initialise en tant que liste si ce n'est pas déjà une liste

                        # Si la classe n'est pas déjà dans la liste, ajoute la classe
                        if classroom_name not in student_classroom:
                            student_classroom.append(classroom_name)

                        # Met à jour la classe de l'étudiant dans la base de données
                        self.student_collection.update_one(
                            {'_id': student_id},
                            {'$set': {'classroom_name': student_classroom}}
                        )

                        # Ajouter les informations complètes de l'étudiant à la liste
                        student_info['classroom_name'] = student_classroom
                        number_of_students.append(student_info)

                # Décrémenter le nombre de places disponibles
                if available_places > 0:
                    available_places -= len(students)

                # Mettre à jour le champ number_of_students et number_of_places_available dans la base de données
                self.classroom_collection.update_one(
                    {'classroom_name': classroom_name},
                    {'$set': {'number_of_students': number_of_students, 'number_of_places_available': available_places}}
                )

                student_names = ', '.join([f"{student['first_name']} {student['last_name']}" for student in students])
                print(f"Étudiant(e) {student_names} ajouté(e) à la classe {classroom_name} avec succès !")
            except Exception as e:
                print(
                    f"Une erreur s'est produite lors de l'ajout de l'étudiant à la classe {classroom_name} : "
                    f"{str(e)}"
                )
        else:
            print(f"Aucune classe trouvée avec le nom {classroom_name}.")

    def remove_student_from_classroom_database_controller(self, classroom_name, student_info):
        classroom = self.get_classroom_database_controller(classroom_name)
        if classroom:
            try:
                # Assure que number_of_students est une liste
                number_of_students = (
                    classroom['number_of_students']
                    if isinstance(classroom['number_of_students'], list)
                    else []
                )

                # Nombre de places disponibles
                available_places = classroom['number_of_places_available']

                # Recherche de l'étudiant par son ID
                for student in number_of_students:
                    if student['_id'] == student_info['_id']:
                        # Récupération du nom de l'étudiant
                        student_name = f"{student['first_name']} {student['last_name']}"

                        # Suppression de l'étudiant de la liste
                        number_of_students.remove(student)

                        # Incrémenter le nombre de places disponibles
                        available_places += 1

                        # Mettre à jour le champ number_of_students
                        # et number_of_places_available dans la base de données
                        self.classroom_collection.update_one(
                            {'classroom_name': classroom_name},
                            {
                                '$set': {
                                    'number_of_students': number_of_students,
                                    'number_of_places_available': available_places
                                }
                            }
                        )

                        print(f"L'étudiant {student_name} a été supprimé de la classe {classroom_name} avec succès !")
                        return

                print(f"Aucun étudiant trouvé avec l'ID {student_info['_id']} dans la classe {classroom_name}.")
            except Exception as e:
                print(
                    f"Une erreur s'est produite lors de la suppression de l'étudiant de la classe "
                    f"{classroom_name} : {str(e)}"
                )
        else:
            print(f"Aucune classe trouvée avec le nom {classroom_name}.")

    def delete_classroom_database_controller(self, classroom_name):
        classroom = self.classroom_collection.find_one({'classroom_name': classroom_name})
        if classroom:
            try:
                self.classroom_collection.delete_one({'classroom_name': classroom_name})
                print(f"La classe {classroom_name} a été supprimé avec succès!")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la suppression de la classe : {str(e)}")
        else:
            print(f"Aucune classe trouvé avec le nom {classroom_name}.")

    def calculate_classroom_average_database_controller(self, classroom_name):
        # Récupére les étudiants dans la classe spécifiée
        students = self.get_students_in_classroom_database_controller(classroom_name)

        if students:
            # Récupére les notes de tous les étudiants dans une liste
            all_grades = [grade for student in students for grade in student.get('grades', [])]

            # Calcule la moyenne des notes de tous les étudiants
            if all_grades:
                return sum(all_grades) / len(all_grades)

        # Retourne None si aucune donnée n'est trouvée ou si aucune note n'est disponible
        return None


"""
    def calculate_student_average_database_controller(self, student_name):
        student = self.student_collection.find_one({'first_name': student_name})

        if student:
            grades = student.get('grades', [])
            if grades:
                return sum(grades) / len(grades)
        return None
"""
