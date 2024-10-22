# tests/tests_models/test_classroom_models.py
import pytest
from models.classroom_models import ClassroomModel


class TestClassroomModels:

    @pytest.fixture
    def classroom(self):
        # Créer une instance de ClassroomModel avant chaque test
        return ClassroomModel("Math Class", 30)

    def test_classroom_initialization(self, classroom):
        assert classroom.classroom_name == "Math Class"
        assert classroom.number_of_places_available == 30
        assert classroom.number_of_students == []

    def test_add_students_classroom(self, classroom):
        students = [
            {'first_name': 'Alice', 'last_name': 'Johnson'},
            {'first_name': 'Bob', 'last_name': 'Smith'}
        ]

        classroom.add_students_classroom(students)
        assert len(classroom.number_of_students) == 2

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
        classroom.update_classroom_info(classroom_name="Science Class", number_of_places_available=25)
        assert classroom.classroom_name == "Science Class"
        assert classroom.number_of_places_available == 25

    def test_remove_student_classroom(self, classroom):
        student = {'first_name': 'Alice', 'last_name': 'Johnson'}
        classroom.add_students_classroom([student])
        classroom.remove_student_classroom(student)
        assert len(classroom.number_of_students) == 0

    def test_validate_input_data_classroom(self, classroom):
        classroom.classroom_name = ""
        assert not classroom.validate_input_data_classroom()

        classroom.classroom_name = "Valid Name"
        classroom.number_of_places_available = -1
        assert not classroom.validate_input_data_classroom()
