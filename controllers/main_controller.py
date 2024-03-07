from views.main_menu_views import MainMenuView
from controllers.student_controller import StudentDatabaseController
from controllers.classroom_controller import ClassroomDatabaseController


class MainController:

    def __init__(self):
        self.student_database_controller = StudentDatabaseController()
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