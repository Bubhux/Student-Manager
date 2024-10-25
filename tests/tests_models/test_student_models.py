# tests/tests_models/test_student_models.py
import pytest
from models.student_models import StudentModel


class TestStudentModel:

    @pytest.fixture
    def student(self):
        # Créer une instance de StudentModel avant chaque test
        return StudentModel(first_name="John", last_name="Doe", grades=[15, 18, 12], classroom_name="Math Class", lessons=["Math", "Science"])

    def test_initialization(self, student):
        # Vérifier que l'initialisation fonctionne correctement
        assert student.first_name == "John"
        assert student.last_name == "Doe"
        assert student.grades == [15, 18, 12]
        assert student.classroom_name == "Math Class"
        assert student.lessons == ["Math", "Science"]

    def test_update_student_info(self, student):
        # Mise à jour avec de nouvelles informations
        student.update_student_info(first_name="Jane", last_name="Smith", grades=[10, 14], classroom_name="Science Class", lessons=["Physics"])
        assert student.first_name == "Jane"
        assert student.last_name == "Smith"
        assert student.grades == [10, 14]
        assert student.classroom_name == "Science Class"
        assert student.lessons == ["Physics"]

        # Mise à jour partielle (seulement le prénom et les notes)
        student.update_student_info(first_name="Alice", grades=[16, 19])
        assert student.first_name == "Alice"
        assert student.last_name == "Smith"  # Devrait rester inchangé
        assert student.grades == [16, 19]

    def test_validate_input_data_student_valid_grades(self, student):
        # Notes valides
        student.grades = [0, 15, 20]
        assert student.validate_input_data_student() is True

    def test_validate_input_data_student_invalid_grades(self, student):
        # Notes invalides (hors des limites)
        student.grades = [25, -5, 10]
        assert student.validate_input_data_student() is False

        # Notes contenant des valeurs non numériques
        student.grades = ["A", "15", None]
        assert student.validate_input_data_student() is False

    def test_validate_input_data_student_empty_grades(self, student):
        # Liste de notes vides
        student.grades = []
        assert student.validate_input_data_student() is True

    def test_validate_input_data_student_with_none_grades(self, student):
        # Liste de notes avec None et chaînes vides
        student.grades = [None, '']
        assert student.validate_input_data_student() is True  # Devrait ignorer ces valeurs
