from pymongo import MongoClient


class DatabaseController:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # Connexion au serveur MongoDB
        self.db = self.client['StudentCG']  # Sélection de la base de données
        self.collection = self.db['students']  # Sélection de la collection

    def add_student(self, student_data):
        try:
            self.collection.insert_one(student_data)
            print(f"L'étudiant {student_data['first_name']} {student_data['last_name']} a été ajouté avec succès!")
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'ajout de l'étudiant : {str(e)}")

    def get_student(self, student_name):
        return self.collection.find_one({'first_name': student_name})

    def get_all_students(self):
        students = list(self.collection.find())
        if not students:
            return []
        return students

    def update_student_grades(self, student_name, new_grades):
        # Recherche de l'étudiant par son nom complet ou son prénom uniquement
        student = self.collection.find_one({'$or': [{'first_name': student_name}, {'last_name': student_name}]})

        if student:
            try:
                self.collection.update_one({'_id': student['_id']}, {'$set': {'grades': new_grades}})
                print(f"Les notes de l'étudiant {student_name} ont été mises à jour avec succès!")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la mise à jour des notes de l'étudiant : {str(e)}")
        else:
            print(f"Aucun étudiant trouvé avec le nom {student_name}. Vérifiez le nom de l'étudiant.")

    def delete_student(self, student_name):
        student = self.collection.find_one({'first_name': student_name})
        if student:
            try:
                self.collection.delete_one({'first_name': student_name})
                print(f"L'étudiant {student_name} a été supprimé avec succès!")
            except Exception as e:
                print(f"Une erreur s'est produite lors de la suppression de l'étudiant : {str(e)}")
        else:
            print(f"Aucun étudiant trouvé avec le nom {student_name}.")

    def calculate_student_average(self, student_name):
        student = self.collection.find_one({'first_name': student_name})

        if student:
            grades = student.get('grades', [])
            if grades:
                return sum(grades) / len(grades)
        return None

    def calculate_class_average(self):
        all_students = self.collection.find()
        grades = [student.get('grades', []) for student in all_students]
        all_grades = [grade for sublist in grades for grade in sublist]

        if all_grades:
            return sum(all_grades) / len(all_grades)
        return None
