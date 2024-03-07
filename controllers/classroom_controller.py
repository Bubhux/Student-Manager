from pymongo import MongoClient

from models.student_models import StudentModel
from models.classroom_models import ClassroomModel


class ClassroomDatabaseController:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # Connexion au serveur MongoDB
        self.db_name = 'StudentCG'  # Nom de la base de données
        self.db = self.client[self.db_name]  # Sélection de la base de données
        self.classroom_collection = self.db['classrooms'] # Sélection de la collection

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
        return self.classroom_collection.find_one({'classroom_name': classroom_name})

    def get_all_classrooms_database_controller(self):
        classrooms = list(self.classroom_collection.find())
        if not classrooms:
            return []
        return classrooms

    def update_classroom_info_database_controller(self, classroom_name, new_classroom_data):
        # Recherche de la classe par son nom
        classroom = self.classroom_collection.find_one({'classroom_name': classroom_name})

        if classroom:
            try:
                # Création d'une instance de ClassroomModel avec les nouvelles données
                updated_classroom = ClassroomModel(classroom_name=new_classroom_data['classroom_name'],
                                                   number_of_places_available=new_classroom_data['number_of_places_available']
                )

                # Mise à jour des données de la classe dans la base de données
                self.classroom_collection.update_one({'classroom_name': classroom_name}, {'$set': new_classroom_data})
                print(f"Les informations de la classe {classroom_name} ont été mises à jour avec succès!")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la mise à jour des informations de la classe : {str(e)}")
        else:
            print(f"Aucune classe trouvée avec le nom {classroom_name}. Vérifiez le nom de la classe.")


"""
    def calculate_student_average_database_controller(self, student_name):
        student = self.student_collection.find_one({'first_name': student_name})

        if student:
            grades = student.get('grades', [])
            if grades:
                return sum(grades) / len(grades)
        return None

    def calculate_class_average_database_controller(self, classroom_name):
        # Récupére les données de la classe spécifiée par classroom_name
        classroom_data = self.classroom_collection.find_one({'classroom_name': classroom_name})

        if classroom_data:
            # Extraire la liste des étudiants de la classe
            students = classroom_data.get('students', [])

            # Récupérer les notes de tous les étudiants dans une liste
            all_grades = [grade for student in students for grade in student.get('grades', [])]

            # Calculer la moyenne des notes de tous les étudiants
            if all_grades:
                return sum(all_grades) / len(all_grades)
        
        # Retourner None si aucune donnée n'est trouvée ou si aucune note n'est disponible
        return None
"""