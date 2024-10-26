# tests/tests_models/test_student_models.py
import pytest
from models.student_models import StudentModel


class TestStudentModel:

    @pytest.fixture
    def student(self):
        # Créer une instance de StudentModel avant chaque test
        return StudentModel(first_name="John", last_name="Doe", grades=[15, 18, 12], classroom_name="Math Class", lessons=["Math", "Science"])

    def test_initialization(self, student):
        # Vérifie que l'initialisation fonctionne correctement
        assert student.first_name == "John"
        assert student.last_name == "Doe"
        assert student.grades == [15, 18, 12]
        assert student.classroom_name == "Math Class"
        assert student.lessons == ["Math", "Science"]

    def test_str_method(self, student):
        # Vérifie que __str__ retourne la chaîne correcte
        assert str(student) == "Étudiant John Doe"

        # Test avec un étudiant sans nom de famille
        student_with_no_last_name = StudentModel(first_name="Jane")
        assert str(student_with_no_last_name) == "Étudiant Jane None"

    def test_update_student_info_all_fields(self, student):
        # Mise à jour avec tous les champs
        student.update_student_info(first_name="Jane", last_name="Smith", grades=[10, 14], classroom_name="Science Class", lessons=["Physics"])
        assert student.first_name == "Jane"
        assert student.last_name == "Smith"
        assert student.grades == [10, 14]
        assert student.classroom_name == "Science Class"
        assert student.lessons == ["Physics"]

    def test_update_student_info_partial_update(self, student):
        # Mise à jour partielle (seulement le prénom et les notes)
        student.update_student_info(first_name="Alice", grades=[16, 19])
        assert student.first_name == "Alice"
        assert student.last_name == "Doe"  # Devrait rester inchangé
        assert student.grades == [16, 19]
        assert student.classroom_name == "Math Class"  # Devrait rester inchangé

    def test_update_student_info_no_update(self, student):
        # Ne rien mettre à jour (tous les champs sont None)
        student.update_student_info()
        assert student.first_name == "John"  # Devrait rester inchangé
        assert student.last_name == "Doe"
        assert student.grades == [15, 18, 12]
        assert student.classroom_name == "Math Class"
        assert student.lessons == ["Math", "Science"]

    def test_update_student_info_none_values(self, student):
        # Mise à jour avec des valeurs None explicites
        student.update_student_info(first_name=None, last_name=None, grades=None, classroom_name=None, lessons=None)
        assert student.first_name == "John"  # Devrait rester inchangé
        assert student.last_name == "Doe"
        assert student.grades == [15, 18, 12]
        assert student.classroom_name == "Math Class"
        assert student.lessons == ["Math", "Science"]

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
