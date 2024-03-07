

class ClassroomModel:

    def __init__(self, name, students=None):
        self.name = name
        self.students = students if students is not None else []

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)

    def get_students(self):
        return self.students

    def validate_input_data(self):
        # Ajout de la logique de validation des données de la classe
        # Par exemple, vérifier si le nom de la classe est valide, etc.
        pass
