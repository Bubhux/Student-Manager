# controllers/classroom_controller.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

from models.student_models import StudentModel
from models.classroom_models import ClassroomModel


load_dotenv()

class ClassroomDatabaseController:

    def __init__(self):
        # Vérifie si l'application tourne dans un environnement Docker
        is_docker = os.getenv('DOCKER', 'false').lower() == 'true'

        if is_docker:
            # Utilisation des variables pour Docker
            mongo_host = os.getenv('MONGO_HOST', 'mongo')
            mongo_port = int(os.getenv('MONGO_PORT', 27017))
        else:
            # Utilisation des variables pour un environnement local
            mongo_host = os.getenv('LOCAL_MONGO_HOST', 'localhost')
            mongo_port = int(os.getenv('LOCAL_MONGO_PORT', 27017))

        # Connexion au serveur MongoDB
        self.client = MongoClient(mongo_host, mongo_port)
        self.db_name = os.getenv('MONGO_INITDB_DATABASE', 'StudentCG')  # Nom de la base de données
        self.db = self.client[self.db_name]
        self.student_collection = self.db['students']
        self.classroom_collection = self.db['classrooms']

    def add_classroom_database_controller(self, classroom_data):
        existing_classroom = self.classroom_collection.find_one({'classroom_name': classroom_data['classroom_name']})
        if existing_classroom:
            print(f"Une classe avec le nom {classroom_data['classroom_name']} existe déjà. Impossible d'ajouter la classe.")
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

    def get_students_in_classroom_database_controller(self, classroom_name):
        # Récupère les informations de la classe depuis la base de données
        classroom_info = self.classroom_collection.find_one({'classroom_name': classroom_name})

        if classroom_info:
            # Récupère directement les informations des étudiants de la classe
            students_info = classroom_info.get('number_of_students', [])
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
                number_of_students = classroom['number_of_students'] if isinstance(classroom['number_of_students'], list) else []

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
                        self.student_collection.update_one({'_id': student_id}, {'$set': {'classroom_name': student_classroom}})

                        # Ajouter les informations complètes de l'étudiant à la liste
                        student_info['classroom_name'] = student_classroom
                        number_of_students.append(student_info)

                # Mettre à jour le champ number_of_students dans la base de données
                self.classroom_collection.update_one(
                    {'classroom_name': classroom_name},
                    {'$set': {'number_of_students': number_of_students}}
                )

                student_names = ', '.join([f"{student['first_name']} {student['last_name']}" for student in students])
                print(f"Étudiant(e) {student_names} ajouté(e) à la classe {classroom_name} avec succès !")
            except Exception as e:
                print(f"Une erreur s'est produite lors de l'ajout de l'étudiants à la classe {classroom_name} : {str(e)}")
        else:
            print(f"Aucune classe trouvée avec le nom {classroom_name}.")

    def remove_student_from_classroom_database_controller(self, classroom_name, student_info):
        classroom = self.get_classroom_database_controller(classroom_name)
        if classroom:
            try:
                # Assure que number_of_students est une liste
                number_of_students = classroom['number_of_students'] if isinstance(classroom['number_of_students'], list) else []

                # Recherche de l'étudiant par son ID
                for student in number_of_students:
                    if student['_id'] == student_info['_id']:
                        # Récupération du nom de l'étudiant
                        student_name = f"{student['first_name']} {student['last_name']}"
                        
                        # Suppression de l'étudiant de la liste
                        number_of_students.remove(student)

                        # Mettre à jour le champ number_of_students dans la base de données
                        self.classroom_collection.update_one({'classroom_name': classroom_name}, {'$set': {'number_of_students': number_of_students}})

                        print(f"L'étudiant {student_name} a été supprimé de la classe {classroom_name} avec succès ClassroomControlleur remove_student_from_classroom_database_controller !")
                        return

                print(f"Aucun étudiant trouvé avec l'ID {student_info['_id']} dans la classe {classroom_name}.")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la suppression de l'étudiant de la classe {classroom_name} : {str(e)}")
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