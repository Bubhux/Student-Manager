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
                "number_of_students": 2
            },
            {
                'classroom_name': 'Physique',
                'number_of_places_available': 25,
                "number_of_students": 1
            },
            {
                'classroom_name': 'Chimie',
                'number_of_places_available': 20,
                'number_of_students': 0
            }
        ]

    def __getitem__(self, item):
        if item == 'classrooms':
            return self.classrooms
        elif item == 'students':
            return []
        raise KeyError(f"Collection '{item}' non trouvée.")

    def get_all_classrooms_database_controller(self):
        # Retourne la liste des classes
        return self.classrooms

    def add_classroom_database_controller(self, classroom_data):
        # Ajoute une nouvelle classe à la liste
        self.classrooms.append(classroom_data)

    def update_classroom_info_database_controller(self, classroom_name, new_classroom_data):
        for classroom in self.classrooms:
            if classroom['classroom_name'] == classroom_name:
                classroom.update(new_classroom_data)
                return

    def get_classroom_database_controller(self, classroom_name):
        # Recherche et retour d'une classe spécifique
        for classroom in self.classrooms:
            if classroom['classroom_name'] == classroom_name:
                return classroom
        return None


# Classe de test pour les vues du menu principal des classes
class TestClassroomMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self, mock_mongo_db):
        # Simule une base de données MongoDB avec mongomock
        self.mock_db = mongomock.MongoClient()['test_database']

        # Injecte la base de données fictive dans ClassroomView
        self.view = ClassroomView(self.mock_db)
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

    @patch('click.prompt', side_effect=['Histoire', '10', '0'])
    @patch('click.confirm', return_value=True)
    def test_add_classroom(self, mock_prompt, mock_confirm, capsys):
        # Exécution de la méthode add_classroom
        self.view.add_classroom()

        # Vérification que la classe a bien été ajoutée
        added_classroom = next(
            (classroom for classroom in self.view.classroom_controller.get_all_classrooms_database_controller()
            if classroom['classroom_name'] == 'Histoire'),
            None
        )

        assert added_classroom is not None
        assert added_classroom['classroom_name'] == 'Histoire'
        assert added_classroom['number_of_places_available'] == 10
        assert added_classroom['number_of_students'] == 0

        # Vérification des appels aux mocks
        mock_prompt.assert_called()
        mock_confirm.assert_called()

        # Capture de la sortie après l'ajout de la salle
        captured = capsys.readouterr()

        # Vérification de l'affichage correct de la nouvelle salle
        self.assert_classroom_displayed(captured, "Histoire", 10, 0)

