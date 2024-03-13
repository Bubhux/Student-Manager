

class StudentModel:

    def __init__(self, first_name, last_name=None, grades=None, classroom_name=None, lessons=None):
        self.first_name = first_name
        self.last_name = last_name
        self.grades = grades if grades is not None else []
        self.classroom_name = classroom_name
        self.lessons = lessons if lessons is not None else []

    def __str__(self):
        return f"Étudiant {self.first_name} {self.last_name}"

    def update_student_info(self, first_name=None, last_name=None, grades=None, classroom_name=None, lessons=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if grades:
            self.grades = grades
        if classroom_name:
            self.classroom_name = classroom_name
        if lessons:
            self.lessons = lessons

    def validate_input_data_student(self):
        # Itération à travers chaque note dans la liste des notes de l'étudiant
        for grade in self.grades:
            # Vérifie si la note est une chaîne de caractères vide ou nulle
            if grade == '' or grade is None:
                continue

            try:
                # Convertis la note en un nombre à virgule flottante
                grade = float(grade)
                # Vérifie si la note est comprise entre 0 et 20 inclusivement
                if not 0 <= grade <= 20:
                    # Si la note est en dehors de la plage valide, retourne False
                    return False
            except ValueError:
                # Si la note ne peut pas être convertie en nombre, elle est invalide
                return False

        # Si toutes les notes sont valides ou aucune note n'a été fournie, retourne True
        return True

    def get_value_classroom(self):
        return self.classroom_name

    def set_student_classroom(self, classroom):
        self.classroom_name = classroom_name
