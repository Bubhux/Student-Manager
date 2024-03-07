from pymongo import MongoClient

from models.student_models import StudentModel
from models.classroom_models import ClassroomModel


class StudentDatabaseController:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # Connexion au serveur MongoDB
        self.db_name = 'StudentCG'  # Nom de la base de données
        self.db = self.client[self.db_name]  # Sélection de la base de données
        self.student_collection = self.db['students']  # Sélection de la collection

    def connect_to_database(self):
        try:
            # Vérifie la connexion à la base de données
            self.client.server_info()
            print(f"Connexion à la base de données MongoDB '{self.db_name}' établie avec succès.")
        except Exception as e:
            print("Erreur de connexion à la base de données MongoDB :", str(e))
            raise

    def add_student_database_controller(self, student_data):
        try:
            self.student_collection.insert_one(student_data)
            print(f"L'étudiant {student_data['first_name']} {student_data['last_name']} a été ajouté avec succès!")
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'ajout de l'étudiant : {str(e)}")

    def get_student_database_controller(self, student_name):
        return self.student_collection.find_one({'first_name': student_name})

    def get_all_students_database_controller(self):
        students = list(self.student_collection.find())
        if not students:
            return []
        return students

    def update_student_grades_database_controller(self, student_name, new_grades):
        # Recherche de l'étudiant par son nom complet ou son prénom uniquement
        student = self.student_collection.find_one({'$or': [{'first_name': student_name}, {'last_name': student_name}]})

        if student:
            try:
                self.student_collection.update_one({'_id': student['_id']}, {'$set': {'grades': new_grades}})
                print(f"Les notes de l'étudiant {student_name} ont été mises à jour avec succès!")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la mise à jour des notes de l'étudiant : {str(e)}")
        else:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")

    def update_student_info_database_controller(self, student_name, new_student_data):
        # Recherche de l'étudiant par son nom complet ou son prénom uniquement
        student = self.student_collection.find_one({'$or': [{'first_name': student_name}, {'last_name': student_name}]})

        if student:
            try:
                updated_student = StudentModel(student['first_name'], student['last_name'], student['grades'])
                updated_student.update_student_info(first_name=new_student_data['first_name'], last_name=new_student_data['last_name'], grades=new_student_data['grades'])
                self.student_collection.update_one({'_id': student['_id']}, {'$set': {
                    'first_name': updated_student.first_name,
                    'last_name': updated_student.last_name,
                    'grades': updated_student.grades
                }})
                print(f"Les informations de l'étudiant {student_name} ont été mises à jour avec succès!")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la mise à jour des informations de l'étudiant : {str(e)}")
        else:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")

    def delete_student_database_controller(self, student_name):
        student = self.student_collection.find_one({'first_name': student_name})
        if student:
            try:
                self.student_collection.delete_one({'first_name': student_name})
                print(f"L'étudiant {student_name} a été supprimé avec succès!")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la suppression de l'étudiant : {str(e)}")
        else:
            print(f"Aucun étudiant trouvé avec le nom {student_name}.")

    def calculate_student_average_database_controller(self, student_name):
        student = self.student_collection.find_one({'first_name': student_name})

        if student:
            grades = student.get('grades', [])
            if grades:
                return sum(grades) / len(grades)
        return None

    def calculate_class_average_database_controller(self):
        all_students = self.student_collection.find()
        grades = [student.get('grades', []) for student in all_students]
        all_grades = [grade for sublist in grades for grade in sublist]

        if all_grades:
            return sum(all_grades) / len(all_grades)
        return None
