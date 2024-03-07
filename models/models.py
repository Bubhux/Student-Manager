

class StudentModel:

    def __init__(self, first_name, last_name=None, grades=None):
        self.first_name = first_name
        self.last_name = last_name
        self.grades = grades if grades is not None else []


class StudentManager:

    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def update_grades(self, full_name, new_grades):
        student_to_update = None
        for student in self.students:
            if full_name == student.first_name or full_name == student.first_name + " " + student.last_name:
                student_to_update = student
                break

        if student_to_update is not None:
            student_to_update.grades = new_grades

    def get_all_students(self):
        if not self.students:
            return None
        return self.students

    def calculate_student_average(self, full_name):
        student_to_calculate = None
        for student in self.students:
            if full_name == student.first_name or full_name == student.first_name + " " + student.last_name:
                student_to_calculate = student
                break

        if student_to_calculate is not None:
            if not student_to_calculate.grades:
                return None
            return sum(student_to_calculate.grades) / len(student_to_calculate.grades)
        else:
            return None

    def calculate_class_average(self):
        if not self.students:
            return None

        total_grades = [grade for student in self.students for grade in student.grades]
        average = sum(total_grades) / len(total_grades)
        return average

    def delete_student(self, full_name):
        for student in self.students:
            if full_name.lower() == student.first_name.lower() or full_name.lower() == (student.first_name + " " + student.last_name).lower():
                self.students.remove(student)
