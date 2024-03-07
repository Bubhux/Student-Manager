from views.views import StudentView, MainMenuView
from controllers.database_controller import DatabaseController


class StudentController:

    def __init__(self):
        self.database_controller = DatabaseController()
        self.main_menu = MainMenuView()

    def run_program(self):
        print("run_program")

        self.main_menu.display_main_menu()
        print("run_program_end")

    def add_student(self, name, french, math, geography, history):
        grades = [french, math, geography, history]
        student_data = {'first_name': name, 'grades': grades}
        self.database_controller.add_student(student_data)

    def update_student_grades(self, name, french, math, geography, history):
        new_grades = [french, math, geography, history]
        self.database_controller.update_student_grades(name, new_grades)

    def calculate_student_average(self, name):
        return self.db_controller.calculate_student_average(name)

    def calculate_class_average(self):
        return self.database_controller.calculate_class_average()

    def display_students(self):
        students = self.database_controller.get_all_students()
        return students
