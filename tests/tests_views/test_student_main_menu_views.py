# tests/tests_views/test_student_main_menu_views.py
import pytest
import mongomock
from unittest.mock import patch
from rich.console import Console
from views.student_menu_views import StudentView


# Fixture pour simuler une base de données MongoDB en mémoire
@pytest.fixture
def mock_mongo_db():
    # Utilisation de mongomock pour patcher le serveur MongoDB
    with mongomock.patch(servers=(('localhost', 27017),)):
        yield  # Cette ligne permet de garder le contexte pour les tests


# Classe de simulation pour contrôler les données des étudiants
class MockStudentDatabaseController:

    def __init__(self):
        # Liste d'étudiants fictifs pour les tests
        self.students = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'classroom_name': 'Class A',
                'grades': [12, 10, 15],
                'lessons': [{'name': 'Math', 'grade': 12},
                            {'name': 'Science', 'grade': 10},
                            {'name': 'History', 'grade': 15}]
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'classroom_name': 'Class B',
                'grades': [9, 18, 19],
                'lessons': [{'name': 'English', 'grade': 9},
                            {'name': 'Art', 'grade': 18},
                            {'name': 'Physical Education', 'grade': 19}]
            }
        ]

    def get_all_students_database_controller(self):
        # Retourne la liste des étudiants
        return self.students

    def add_student_database_controller(self, student_data):
        # Ajoute un nouvel étudiant à la liste
        self.students.append(student_data)


# Classe de test pour les vues du menu principal des étudiants
class TestStudentMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self, mock_mongo_db):
        # Initialisation de la vue d'étudiant et de la console avant chaque test
        self.view = StudentView()
        self.view.student_controller = MockStudentDatabaseController()
        self.console = Console()

    def assert_student_displayed(self, captured, first_name, last_name, classroom_name, subjects=None):
        # Fonction utilitaire pour vérifier le nom, prénom, classe et éventuellement les matières
        # Vérification que le nom et prénom de l'étudiant ainsi que sa classe sont affichés
        assert f"{first_name} {last_name}" in captured.out
        assert classroom_name in captured.out

        # Si des matières sont fournies, vérifier également leur affichage
        if subjects:
            for subject in subjects:
                assert subject in captured.out

    @patch('click.prompt', return_value='1')
    def test_display_students(self, mock_prompt, capsys):
        # Teste l'affichage de la liste des étudiants
        self.view.display_students()
        captured = capsys.readouterr()  # Capture la sortie

        assert "Liste des étudiants triés par ordre alphabétique" in captured.out
        # Vérification que les informations sur les étudiants sont correctement affichées
        self.assert_student_displayed(captured, 'John', 'Doe', 'Class A')
        self.assert_student_displayed(captured, 'Jane', 'Smith', 'Class B')

    @patch('click.prompt', return_value='1')
    def test_display_student_informations(self, mock_prompt, capsys):
        # Teste l'affichage des informations détaillées d'un étudiant
        self.view.display_student_informations(self.view.student_controller.get_all_students_database_controller())
        captured = capsys.readouterr()  # Capture la sortie

        assert "Informations sur l'étudiant" in captured.out
        # Vérification que les informations de John Doe et ses matières sont affichées
        self.assert_student_displayed(captured, 'John', 'Doe', 'Class A', ['Math', 'Science', 'History'])

    @patch('click.prompt', side_effect=['invalid_input'])
    def test_invalid_student_selection(self, mock_prompt, capsys):
        # Teste le comportement lors d'une sélection d'étudiant invalide
        self.view.display_student_informations(self.view.student_controller.get_all_students_database_controller())
        captured = capsys.readouterr()  # Capture la sortie

        assert "Aucun étudiant trouvé avec cette entrée." in captured.out  # Vérifie le message d'erreur

    @patch('builtins.input', side_effect=['Alice', 'Wonderland', '0'])
    @patch('click.prompt', side_effect=['Wonderland', '0'])
    @patch('click.confirm', return_value=True)
    def test_add_student(self, mock_input, mock_prompt, mock_confirm):
        # Teste l'ajout d'un nouvel étudiant
        self.view.add_student()

        # Recherche l'étudiant ajouté dans la liste
        added_student = next((student for student in self.view.student_controller.get_all_students_database_controller() if student['first_name'] == 'Alice'), None)

        # Vérification que l'étudiant a été correctement ajouté
        assert added_student is not None
        assert added_student['first_name'] == 'Alice'
        assert added_student['last_name'] == 'Wonderland'
        assert added_student['grades'] == []  # Vérifie que l'étudiant a une liste de notes vide

        # Vérifie que les appels aux mocks ont eu lieu
        mock_input.assert_called()
        mock_prompt.assert_called()
        mock_confirm.assert_called()
