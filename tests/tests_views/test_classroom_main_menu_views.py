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
        self.classrooms = [
            {
                'classroom_name': 'Mathématiques',
                'number_of_places_available': 30,
                "number_of_students": 2,
                "students": [
                    {'_id': '1', 'first_name': 'Alice', 'last_name': 'Brown'},
                    {'_id': '2', 'first_name': 'Bob', 'last_name': 'Yellow'}
                ]
            },
            {
                'classroom_name': 'Physique',
                'number_of_places_available': 25,
                "number_of_students": 1,
                "students": [
                    {'_id': '3', 'first_name': 'Charlie', 'last_name': 'Pink'}
                ]
            },
            {
                'classroom_name': 'Chimie',
                'number_of_places_available': 20,
                'number_of_students': 0,
                "students": []
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

    def get_classroom_by_student_id(self, student_id):
        for classroom in self.classrooms:
            student_list = classroom.get('students', [])
            student_ids = [student['_id'] for student in student_list]
            if student_id in student_ids:
                return classroom['classroom_name']
        return None

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
        classroom = self.get_classroom_database_controller(classroom_name)
        if classroom:
            # Retourne une liste d'ID fictifs pour les étudiants
            return [1, 2] if classroom['number_of_students'] > 0 else []
        return []

    def get_all_students_database_controller(self):
        return self.students

    def add_students_to_classroom_database_controller(self, classroom_name, selected_students):
        # Trouve la classe cible
        classroom = self.get_classroom_database_controller(classroom_name)
        if classroom:
            classroom['students'].extend(selected_students)  # Ajouter les étudiants à la classe
            classroom['number_of_students'] += len(selected_students)  # Mettre à jour le nombre d'étudiants


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

    @patch('click.prompt')
    def test_add_students_to_selected_class_check_student_class_membership(self, mock_prompt, capsys):
        # Prépare les étudiants fictifs
        mock_students = [
            {'_id': '1', 'first_name': 'Alice', 'last_name': 'Brown'},
            {'_id': '2', 'first_name': 'Bob', 'last_name': 'Yellow'},
            {'_id': '3', 'first_name': 'Charlie', 'last_name': 'Pink'}
        ]

        # Injecte des étudiants fictifs dans la classe simulée
        self.classroom_view.student_controller = MagicMock()
        self.classroom_view.student_controller.get_all_students_database_controller.return_value = mock_students

        # Simule les entrées utilisateur
        mock_prompt.side_effect = [
            2,    # Ajoute 2 étudiants
            '1',  # Sélectionne Alice
            '2',  # Sélectionne Bob
            'r'   # Quitte
        ]

        # Appele la méthode à tester
        self.classroom_view.add_students_to_selected_class("Mathématiques")

        # Récupére les données de la classe après l'ajout des étudiants
        classroom = self.classroom_view.classroom_controller.get_classroom_database_controller("Mathématiques")

        # Vérifie que le nombre d'étudiants n'a pas augmenté
        assert classroom['number_of_students'] == 2  # Aucun étudiant n'a été ajouté car ils sont déjà assignés à d'autres classes

        # Vérifie que les messages de confirmation sont affichés
        captured = capsys.readouterr()
        assert "L'étudiant Alice Brown appartient déjà à la classe Mathématiques." in captured.out
        assert "L'étudiant Charlie Pink appartient déjà à la classe Physique." in captured.out

    @patch('click.prompt', side_effect=[1])  # 1 étudiant à ajouter
    def test_add_student_when_no_students_available(self, mock_prompt, capsys):
        classroom_name = "Chimie"

        # Simule l'absence d'étudiants
        self.classroom_view.student_controller = MagicMock()
        self.classroom_view.student_controller.get_all_students_database_controller.return_value = []

        # Appelle la fonction
        self.classroom_view.add_students_to_selected_class(classroom_name)

        # Vérifie que la sortie contient le message d'erreur
        captured = capsys.readouterr()
        assert "Il n'y a pas d'élèves à afficher." in captured.out
"""
    @patch('click.prompt', side_effect=[0, 1, 1])
    def test_add_zero_students(self, mock_prompt, capsys):
        classroom_name = "Chimie"

        # Simule les étudiants disponibles
        self.classroom_view.student_controller = MagicMock()
        self.classroom_view.student_controller.get_all_students_database_controller.return_value = [
            {'_id': 1, 'first_name': 'John', 'last_name': 'Doe'}
        ]

        # Appelle la fonction
        self.classroom_view.add_students_to_selected_class(classroom_name)

        # Vérifie que la sortie contient l'erreur appropriée
        captured = capsys.readouterr()
        assert "Le nombre d'étudiants ne peut pas être 0." in captured.out

    @patch('click.prompt', return_value='Mathématiques')  # On simule un choix de la classe Mathématiques
    def test_add_student_to_class_successfully(self, mock_prompt, capsys):
        # Simuler un étudiant sans classe
        student = {'_id': '4', 'first_name': 'David', 'last_name': 'Green'}

        # Classe cible pour l'ajout de l'étudiant
        classroom_name = 'Mathématiques'

        # Simuler la méthode d'ajout de l'étudiant à la classe
        self.classroom_view.classroom_controller.add_students_to_classroom_database_controller(classroom_name, [student])

        # Vérifier que l'étudiant a bien été ajouté à la classe
        classroom = self.classroom_view.classroom_controller.get_classroom_database_controller(classroom_name)
        assert len(classroom['students']) == 3  # L'étudiant David Green doit être ajouté
        assert any(student['_id'] == '4' for student in classroom['students'])  # Vérifie que David est bien dans la liste des étudiants

        # Vérifier la mise à jour du nombre d'étudiants et de places disponibles
        assert classroom['number_of_students'] == 3  # 3 étudiants dans la classe
        assert classroom['number_of_places_available'] == 29  # 30 places initialement - 1 étudiant ajouté

        # Capture de la sortie après l'ajout de l'étudiant
        captured = capsys.readouterr()

        # Vérifier que le message de succès contient l'étudiant et la classe
        assert "Étudiant(e) David Green ajouté(e) à la classe Mathématiques avec succès !" in captured.out
"""