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
        # Crée une connexion à la base de données une seule fois ici
        is_docker = os.getenv('DOCKER', 'false').lower() == 'true'

        if is_docker:
            MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
            MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
            MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
            MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
            MONGO_DB = os.getenv("MONGO_INITDB_DATABASE")

            mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
            try:
                self.client = MongoClient(mongo_uri)
                self.db = self.client[MONGO_DB]
                print(f"Connexion à la base de données MongoDB '{MONGO_DB}' établie avec succès.")
            except Exception as e:
                print(f"Erreur lors de la connexion à MongoDB : {e}")
                exit(1)
        else:
            mongo_host = os.getenv('LOCAL_MONGO_HOST', 'localhost')
            mongo_port = int(os.getenv('LOCAL_MONGO_PORT', 27017))
            self.client = MongoClient(mongo_host, mongo_port)
            self.db = self.client[os.getenv('MONGO_INITDB_DATABASE', 'StudentCG')]

        # Passe la connexion à vos autres contrôleurs
        self.student_database_controller = StudentDatabaseController(self.db)
        self.classroom_database_controller = ClassroomDatabaseController(self.db)
        self.main_menu = MainMenuView()

    def run_program(self):
        print("run_program")

        # Vérifie d'abord la connexion à la base de données
        self.student_database_controller.connect_to_database()
        self.main_menu.display_main_menu()
        print("run_program_end")

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