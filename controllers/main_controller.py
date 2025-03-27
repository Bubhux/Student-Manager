# controllers/main_controller.py
from views.main_menu_views import MainMenuView
from controllers.student_controller import StudentDatabaseController
from controllers.classroom_controller import ClassroomDatabaseController

from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()


class MainController:

    def __init__(self):
        is_docker = os.getenv('DOCKER', 'false').lower() == 'true'
        MONGO_DB = os.getenv('MONGO_INITDB_DATABASE', 'StudentCG')

        if is_docker:
            MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
            MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
            MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
            MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

            mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
            try:
                self.client = MongoClient(mongo_uri)
                self.db = self.client[MONGO_DB]
                print(f"Connexion de MainController à la base de données MongoDB '{MONGO_DB}' établie avec succès.")
                print("L'application Student Manager tourne dans l'environnement Docker.")
            except Exception as e:
                print(f"MainController erreur lors de la connexion à MongoDB : {e}")
                exit(1)
        else:
            mongo_host = os.getenv('LOCAL_MONGO_HOST', 'localhost')
            mongo_port = int(os.getenv('LOCAL_MONGO_PORT', 27017))
            try:
                self.client = MongoClient(mongo_host, mongo_port)
                self.db = self.client[MONGO_DB]
                print(f"Connexion de MainController à la base de données MongoDB '{MONGO_DB}' établie avec succès.")
                print("L'application Student Manager tourne dans l'environnement local.")
            except Exception as e:
                print(f"MainController erreur lors de la connexion à MongoDB en local : {e}")
                exit(1)

        # Passe la connexion aux autres contrôleurs
        self.student_database_controller = StudentDatabaseController(self.db)
        self.classroom_database_controller = ClassroomDatabaseController(self.db)
        self.main_menu = MainMenuView(self.db)

    def run_program(self):
        print("Lancement de l'application Student Manager.")

        # Vérifie d'abord la connexion à la base de données
        self.student_database_controller.connect_to_database()
        self.classroom_database_controller.connect_to_database()
        self.main_menu.display_main_menu()
        print("Fermeture de l'application Student Manager.")


"""
    def add_student(self, name, french, math, geography, history):
        grades = [french, math, geography, history]
        student_data = {'first_name': name, 'grades': grades}
        self.student_database_controller.add_student(student_data)

    def update_student_grades(self, name, french, math, geography, history):
        new_grades = [french, math, geography, history]
        self.student_database_controller.update_student_grades(name, new_grades)

    def calculate_student_average(self, name):
        return self.student_database_controller.calculate_student_average(name)

    def calculate_class_average(self):
        return self.student_database_controller.calculate_class_average()

    def display_students(self):
        students = self.student_database_controller.get_all_students()
        return students
"""
