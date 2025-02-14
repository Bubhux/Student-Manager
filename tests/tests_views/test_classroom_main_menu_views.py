# tests/tests_views/test_classroom_main_menu_views.py
import pytest
import mongomock
from unittest.mock import patch, MagicMock
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

    def get_students_in_classroom_database_controller(self, classroom_name):
        # Recherche la classe spécifique et retourne le nombre d'étudiants
        classroom = self.get_classroom_database_controller(classroom_name)
        if classroom:
            return classroom.get('number_of_students', 0)
        return 0

    def get_all_students_database_controller(self):
        return self.students

    def add_students_to_classroom_database_controller(self, classroom_name, selected_students):
        # Trouve la classe cible
        classroom = self.get_classroom_database_controller(classroom_name)
        if classroom:
            classroom['number_of_students'] += len(selected_students)


# Classe de test pour les vues du menu principal des classes
class TestClassroomMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self, mock_mongo_db):
        # Simule une base de données MongoDB avec mongomock
        self.mock_db = mongomock.MongoClient()['test_database']

        # Injecte la base de données fictive dans ClassroomView
        self.classroom_view = ClassroomView(self.mock_db)
        self.classroom_view.classroom_controller = MockClassroomDatabaseController()
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
        self.classroom_view.display_classrooms()
        captured = capsys.readouterr()  # Capture la sortie

        assert "Liste des classes triées par ordre alphabétique" in captured.out
        # Vérifie que les classes et étudiants fictifs sont affichés
        self.assert_classroom_displayed(captured, "Mathématiques", 30, 2)
        self.assert_classroom_displayed(captured, "Physique", 25, 1)
        self.assert_classroom_displayed(captured, "Chimie", 20, 0)

    @patch('click.prompt', side_effect=['Histoire', '10', '0'])
    @patch('click.confirm', return_value=True)
    def test_add_classroom(self, mock_prompt, mock_confirm, capsys):
        # Exécution de la méthode add_classroom
        self.classroom_view.add_classroom()

        # Vérification que la classe a bien été ajoutée
        added_classroom = next(
            (classroom for classroom in self.classroom_view.classroom_controller.get_all_classrooms_database_controller()
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

    @patch('click.prompt', side_effect=['1', 'Chimie avancées', '35', '5'])
    @patch('click.confirm', side_effect=[True, True])
    def test_update_classroom_info(self, mock_confirm, mock_prompt, capsys):
        # Exécution de la méthode `update_classroom_info`
        self.classroom_view.update_classroom_info()

        # Vérification que les informations de la classe ont été mises à jour
        updated_classroom = next(
            (classroom for classroom in self.classroom_view.classroom_controller.get_all_classrooms_database_controller()
            if classroom['classroom_name'] == 'Chimie avancées'),
            None
        )

        assert updated_classroom is not None
        assert updated_classroom['classroom_name'] == 'Chimie avancées'
        assert int(updated_classroom['number_of_places_available']) == 35  # Convert to int
        assert int(updated_classroom['number_of_students']) == 5

        # Vérification des appels aux mocks
        mock_prompt.assert_called()
        mock_confirm.assert_called()

        # Capture de la sortie après la mise à jour de la salle
        captured = capsys.readouterr()

        # Vérification de l'affichage correct des nouvelles informations
        self.assert_classroom_displayed(captured, "Chimie avancées", 35, 5)

    @patch('click.prompt', side_effect=['1', 'r'])
    @patch('views.classroom_menu_views.ClassroomView.display_available_classes')
    @patch('views.classroom_menu_views.ClassroomView.add_students_to_selected_class')
    def test_add_students_to_classroom(self, mock_add_students, mock_display_classes, mock_prompt, capsys):
        # Configure les mocks
        mock_display_classes.return_value = None  # Simule l'affichage des classes disponibles
        mock_add_students.return_value = None  # Simule l'ajout d'étudiants à une classe

        # Appelle la méthode à tester
        self.classroom_view.add_students_to_classroom()

        # Vérifie que les fonctions dépendantes ont été appelées correctement
        mock_display_classes.assert_called_once()  # Vérifie que display_available_classes a été appelée
        mock_add_students.assert_not_called()  # Ajout non effectué car "r" a été choisi au prompt final

        # Capture et vérifie la sortie console
        captured = capsys.readouterr()
        assert "Afficher les classes disponibles" in captured.out
        assert "Retour au menu précédent" in captured.out

    @patch('click.prompt', side_effect=['1', 'r'])
    def test_display_available_classes(self, mock_prompt, capsys):
        self.classroom_view.display_available_classes()

        # Capture la sortie console
        captured = capsys.readouterr()

        # Vérifie que les classes sont affichées
        assert "Classes disponibles triées par ordre alphabétique" in captured.out
        assert "Chimie" in captured.out
        assert "Mathématiques" in captured.out
        assert "Physique" in captured.out

    @patch('click.prompt', side_effect=[2, 1, 3])  # 2 étudiants à ajouter, choix des étudiants 1 et 3
    def test_add_students_to_selected_class(self, mock_prompt, capsys):
        classroom_name = "Chimie"

        # Ajoute des étudiants fictifs à la classe "Chimie"
        self.classroom_view.classroom_controller.classrooms[2]['number_of_students'] = 2  # Classe "Chimie" a maintenant 2 étudiants
        self.classroom_view.student_view = MagicMock()  # S'assure que student_view est bien défini et utilisé
        self.classroom_view.student_view.student_controller.students = [
            {'first_name': 'John', 'last_name': 'Doe'},
            {'first_name': 'Jane', 'last_name': 'Smith'},
            {'first_name': 'Alice', 'last_name': 'Johnson'}
        ]  # Ajoute des étudiants fictifs

        # Appelle la méthode à tester en utilisant self.classroom_view
        self.classroom_view.add_students_to_selected_class(classroom_name)

        # Vérifie que le nombre d'étudiants dans la classe "Chimie" est bien 2 après l'ajout
        classroom = self.classroom_view.classroom_controller.get_classroom_database_controller(classroom_name)
        assert classroom['number_of_students'] == 2  # La classe "Chimie" doit avoir 2 étudiants
