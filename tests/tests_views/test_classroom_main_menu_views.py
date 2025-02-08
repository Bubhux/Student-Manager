# tests/tests_views/test_classroom_main_menu_views.py
import pytest
import mongomock
from unittest.mock import patch
from rich.console import Console
from views.classroom_menu_views import ClassroomView
import re


# Fixture pour simuler une base de données MongoDB en mémoire
@pytest.fixture
def mock_mongo_db():
    # Utilisation de mongomock pour patcher le serveur MongoDB
    with mongomock.patch(servers=(('localhost', 27017),)):
        yield  # Cette ligne permet de garder le contexte pour les tests


# Classe de simulation pour contrôler les données des classes
class MockClassroomDatabaseController:

    def __init__(self):
        # Liste des classes fictifs pour les tests
        self.classrooms = [
            {
                'classroom_name': 'Mathématiques',
                'number_of_places_available': 30,
                "number_of_students": [2]
            },
            {
                'classroom_name': 'Physique',
                'number_of_places_available': 25,
                "number_of_students": [1]
            },
            {
                'classroom_name': 'Chimie',
                'number_of_places_available': 20,
                'number_of_students': []
            }
        ]

    def get_all_classrooms_database_controller(self):
        # Retourne la liste des classes
        return self.classrooms


# Classe de test pour les vues du menu principal des classes
class TestClassroomMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self, mock_mongo_db):
        # Initialisation de la vue de la classe et de la console avant chaque test
        self.view = ClassroomView()
        self.view.classroom_controller = MockClassroomDatabaseController()
        self.console = Console()

    def clean_output(self, output):
        return re.sub(r'\x1b\[[0-9;]*m', '', output)  # Supprime les codes d'échappement ANSI

    def remove_ansi_sequences(self, text):
        ansi_escape = re.compile(r'\x1b\[([0-9]+)(;[0-9]+)*m')
        return ansi_escape.sub('', text)

    def assert_classroom_displayed(self, captured, classroom_name, number_of_places_available, number_of_students):
        # Vérification que les informations sur les classes et les étudiants sont correctement affichées
        assert classroom_name in captured.out
        assert str(number_of_places_available) in captured.out
        assert str(number_of_students) in captured.out

    @patch('click.prompt', return_value='1')
    def test_display_classrooms(self, mock_prompt, capsys):
        # Teste l'affichage de la liste des classes
        self.view.display_classrooms()
        captured = capsys.readouterr()  # Capture la sortie

        assert "Liste des classes triées par ordre alphabétique" in captured.out
        # Vérifie que les classes et étudiants fictifs sont affichés
        self.assert_classroom_displayed(captured, "Mathématiques", 30, 1)
        self.assert_classroom_displayed(captured, "Physique", 25, 1)
        self.assert_classroom_displayed(captured, "Chimie", 20, 0)
