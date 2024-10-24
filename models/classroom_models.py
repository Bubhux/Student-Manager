# models/classroom_models.py


class ClassroomModel:

    def __init__(self, classroom_name, number_of_places_available=0, number_of_students=None):
        self.classroom_name = classroom_name
        self.number_of_places_available = number_of_places_available
        self.number_of_students = number_of_students if number_of_students is not None else []

    def __str__(self):
        return f"Classe : {self.classroom_name}, Nombre d'étudiants : {len(self.number_of_students)}"

    def add_students_classroom(self, students):
        self.number_of_students.extend(students)

    def sort_students_alphabetically(self):
        self.number_of_students = sorted(self.number_of_students, key=lambda x: x['first_name'])

    def update_classroom_info(self, classroom_name=None, number_of_places_available=None, number_of_students=None):
        if classroom_name:
            self.classroom_name = classroom_name
        if number_of_places_available is not None:
            self.number_of_places_available = number_of_places_available
        if number_of_students is not None:
            self.number_of_students = number_of_students

    def get_students_classroom(self):
        return self.number_of_students

    def remove_student_classroom(self, student):
        if student in self.number_of_students:
            self.number_of_students.remove(student)

    def validate_input_data_classroom(self):

        if not self.classroom_name:
            print("Le nom de la classe ne peut pas être vide.")
            return False

        if self.number_of_places_available < 0:
            print("Le nombre d'étudiants ne peut pas être négatif.")
            return False

        return True

    def count_students_classroom(self):
        return len(self.number_of_students)
