# tests/tests_models/test_classroom_models.py
import pytest
from models.classroom_models import ClassroomModel


class TestClassroomModels:

    @pytest.fixture
    def classroom(self):
        return ClassroomModel("Math Class", 30)

    def test_classroom_initialization(self, classroom):
        assert classroom.classroom_name == "Math Class"
        assert classroom.number_of_places_available == 30
        assert classroom.number_of_students == []

    def test_classroom_str(self, classroom):
        # Test de la méthode __str__
        assert str(classroom) == "Classe : Math Class, Nombre d'étudiants : 0"

        # Ajoute des étudiants et tester de nouveau
        students = [
            {'first_name': 'Alice', 'last_name': 'Johnson'},
            {'first_name': 'Bob', 'last_name': 'Smith'}
        ]

        classroom.add_students_classroom(students)
        assert str(classroom) == "Classe : Math Class, Nombre d'étudiants : 2"

    @pytest.mark.parametrize("students, expected_count", [
        ([{'first_name': 'Alice', 'last_name': 'Johnson'}], 1),
        ([{'first_name': 'Alice', 'last_name': 'Johnson'}, {'first_name': 'Bob', 'last_name': 'Smith'}], 2),
        ([], 0)
    ])
    def test_add_students_classroom(self, classroom, students, expected_count):
        classroom.add_students_classroom(students)
        assert len(classroom.number_of_students) == expected_count

    @pytest.mark.parametrize("initial_students, student_to_remove, expected_count", [
        ([{'first_name': 'Alice', 'last_name': 'Johnson'}], {'first_name': 'Alice', 'last_name': 'Johnson'}, 0),
        ([{'first_name': 'Alice', 'last_name': 'Johnson'}], {'first_name': 'John', 'last_name': 'Doe'}, 1),
        ([], {'first_name': 'John', 'last_name': 'Doe'}, 0)
    ])
    def test_remove_student_classroom(self, classroom, initial_students, student_to_remove, expected_count):
        classroom.add_students_classroom(initial_students)
        classroom.remove_student_classroom(student_to_remove)
        assert len(classroom.number_of_students) == expected_count

    @pytest.mark.parametrize("classroom_name, number_of_places, expected", [
        ("", 30, False),  # Nom de classe vide
        ("Math Class", -1, False),  # Nombre de places négatif
        ("Valid Name", 20, True)  # Cas valide
    ])
    def test_validate_input_data_classroom(self, classroom, classroom_name, number_of_places, expected):
        classroom.classroom_name = classroom_name
        classroom.number_of_places_available = number_of_places
        assert classroom.validate_input_data_classroom() == expected

    def test_sort_students_alphabetically(self, classroom):
        students = [
            {'first_name': 'Bob', 'last_name': 'Smith'},
            {'first_name': 'Alice', 'last_name': 'Johnson'}
        ]

        classroom.add_students_classroom(students)
        classroom.sort_students_alphabetically()
        assert classroom.number_of_students[0]['first_name'] == 'Alice'
        assert classroom.number_of_students[1]['first_name'] == 'Bob'

    def test_update_classroom_info(self, classroom):
        # Test mise à jour avec tous les paramètres
        classroom.update_classroom_info(classroom_name="Science Class", number_of_places_available=25)
        assert classroom.classroom_name == "Science Class"
        assert classroom.number_of_places_available == 25

        # Test mise à jour avec certains paramètres absents
        classroom.update_classroom_info(classroom_name="History Class")
        assert classroom.classroom_name == "History Class"
        assert classroom.number_of_places_available == 25  # doit rester inchangé

        classroom.update_classroom_info(number_of_places_available=20)
        assert classroom.number_of_places_available == 20

    def test_update_classroom_info_with_students(self, classroom):
        # Initialisation avec des étudiants
        students = [
            {'first_name': 'Alice', 'last_name': 'Johnson'},
            {'first_name': 'Bob', 'last_name': 'Smith'}
        ]

        classroom.update_classroom_info(number_of_students=students)

        # Vérification de la mise à jour de la liste des étudiants
        assert len(classroom.number_of_students) == 2
        assert classroom.number_of_students[0]['first_name'] == 'Alice'

    def test_update_classroom_info_without_students(self, classroom):
        # Initialise avec une liste d'étudiants
        students = [{'first_name': 'Alice', 'last_name': 'Johnson'}]
        classroom.update_classroom_info(number_of_students=students)

        # Appele update sans modifier les étudiants
        classroom.update_classroom_info(classroom_name="History Class")

        # Vérifie que la liste d'étudiants n'a pas changé
        assert len(classroom.number_of_students) == 1
        assert classroom.number_of_students[0]['first_name'] == 'Alice'

    def test_update_classroom_info_with_none_students(self, classroom):
        # Initialise avec une liste d'étudiants
        students = [{'first_name': 'Alice', 'last_name': 'Johnson'}]
        classroom.update_classroom_info(number_of_students=students)

        # Passe None pour ne pas modifier la liste d'étudiants
        classroom.update_classroom_info(number_of_students=None)

        # Vérifie que la liste d'étudiants reste inchangée
        assert len(classroom.number_of_students) == 1
        assert classroom.number_of_students[0]['first_name'] == 'Alice'

    def test_get_students_classroom(self, classroom):
        # Ajoute des étudiants
        students = [{'first_name': 'Alice', 'last_name': 'Johnson'}]
        classroom.update_classroom_info(number_of_students=students)

        # Vérifie que get_students_classroom retourne la liste correcte
        students_list = classroom.get_students_classroom()
        assert len(students_list) == 1
        assert students_list[0]['first_name'] == 'Alice'

    def test_remove_student_classroom(self, classroom):
        student = {'first_name': 'Alice', 'last_name': 'Johnson'}
        classroom.add_students_classroom([student])

        # Suppression de l'étudiant existant
        classroom.remove_student_classroom(student)
        assert len(classroom.number_of_students) == 0

        # Suppression d'un étudiant qui n'existe pas
        non_existing_student = {'first_name': 'John', 'last_name': 'Doe'}
        classroom.remove_student_classroom(non_existing_student)  # Ne devrait pas lever d'exception
        assert len(classroom.number_of_students) == 0
