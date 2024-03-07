

class ClassroomModel:

    def __init__(self, classroom_name, number_of_places_available=0, number_of_students=None):
        """
            Initialise une instance de ClassroomModel.

            Args:
                classroom_name (str): Le nom de la classe.
                number_of_students (int): Le nombre d'étudiants dans la classe par défaut 0.
                students (list, optional): Liste des étudiants de la classe. Par défaut, None.
        """
        self.classroom_name = classroom_name
        self.number_of_places_available = number_of_places_available
        self.number_of_students = number_of_students if number_of_students is not None else []

    def __str__(self):
        """
            Retourne une représentation sous forme de chaîne de caractères de la classe.
        """
        return f"Classe : {self.classroom_name}, Nombre d'étudiants : {len(self.number_of_students)}"

    def add_student_classroom(self, student):
        """
            Ajoute un étudiant à la classe.

            Args:
                student (StudentModel): L'objet représentant l'étudiant à ajouter.
        """
        self.students.append(student)

    def update_classroom_info(self, classroom_name=None, number_of_places_available=None, number_of_students=None):
        if classroom_name:
            self.classroom_name = classroom_name
        if number_of_places_available:
            self.number_of_places_available = number_of_places_available
        if students:
            self.students = students

    def remove_student_classroom(self, student):
        """
            Supprime un étudiant de la classe.

            Args:
                student (StudentModel): L'objet représentant l'étudiant à supprimer.
        """
        if student in self.number_of_students:
            self.students.remove(student)

    def get_students_classroom(self):
        """
            Récupère la liste des étudiants dans la classe.

            Returns:
                list: Liste des objets StudentModel représentant les étudiants dans la classe.
        """
        return self.number_of_students

    def validate_input_data_classroom(self):
        """
            Valide les données d'entrée pour la classe.
            
            Returns:
                bool: True si les données sont valides, False sinon.
        """
        if not self.classroom_name:
            print("Le nom de la classe ne peut pas être vide.")
            return False
        
        if self.number_of_places_available < 0:
            print("Le nombre d'étudiants ne peut pas être négatif.")
            return False

        return True

    def count_students_classroom(self):
        """
            Compte le nombre d'étudiants dans la classe.

            Returns:
                int: Le nombre d'étudiants dans la classe.
        """
        return len(self.number_of_students)
