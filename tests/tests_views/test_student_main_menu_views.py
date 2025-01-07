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

    def get_student_database_controller(self, student_name):
        # Simule la récupération d'un étudiant par nom
        for student in self.students:
            full_name = f"{student['first_name']} {student['last_name']}"
            if student_name == full_name or student_name == student['first_name']:
                return student
        return None  # Si l'étudiant n'est pas trouvé

    def update_student_info_database_controller(self, student_name, updated_student_data):
        # Met à jour les informations de l'étudiant
        for index, student in enumerate(self.students):
            full_name = f"{student['first_name']} {student['last_name']}"
            if student_name == full_name or student_name == student['first_name']:
                self.students[index] = updated_student_data
                break

    def update_student_grades_database_controller(self, student_name, new_grades):
        # Met à jour les notes de l'étudiant
        for student in self.students:
            full_name = f"{student['first_name']} {student['last_name']}"
            if student_name == full_name or student_name == student['first_name']:
                student['lessons'] = new_grades  # Met à jour les leçons avec les nouvelles notes
                break


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

        # Si des matières sont fournies, vérifie également leur affichage
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

    @patch("click.prompt")
    @patch("click.confirm")
    def test_add_subject_to_student(self, mock_confirm, mock_prompt, capsys):
        # Simulation des inputs utilisateur pour click.prompt
        mock_prompt.side_effect = ["John Doe", "Physics", "18"]

        # Simulation de la confirmation utilisateur pour click.confirm
        mock_confirm.return_value = True

        # Exécution de la méthode add_subject_to_student
        self.view.add_subject_to_student()

        # Capture de la sortie console pour validation
        captured = capsys.readouterr()

        # Vérification que les bonnes informations sont affichées dans la console
        assert "Résumé des informations saisies" in captured.out
        assert "John Doe" in captured.out
        assert "Physics" in captured.out
        assert "18.0" in captured.out

        # Vérification que la matière a bien été ajoutée à l'étudiant
        student = self.view.student_controller.students[0]
        assert any(subject['name'] == "Physics" and subject['grade'] == 18.0 for subject in student['lessons'])

    @patch("click.prompt")
    @patch("click.confirm")
    def test_update_student_grades(self, mock_confirm, mock_prompt, capsys):
        # Simule les inputs utilisateur pour click.prompt
        # Simule la saisie du nom de l'étudiant et des nouvelles notes
        mock_prompt.side_effect = [
            "John Doe",  # Nom de l'étudiant
            "16",        # Nouvelle note pour Math
            "12",        # Nouvelle note pour Science
            "15"         # Nouvelle note pour History
        ]

        # Simule la confirmation de la mise à jour des notes
        mock_confirm.return_value = True

        # Exécution de la méthode update_student_grades
        self.view.update_student_grades()

        # Capture de la sortie console pour validation
        captured = capsys.readouterr()

        # Vérifie que les bonnes informations sont affichées dans la console
        assert "Notes modifiées" in captured.out
        assert "Nouvelle note de Math : 16.0" in captured.out
        assert "Nouvelle note de Science : 12.0" in captured.out
        assert "Nouvelle note de History : 15.0" in captured.out
        assert "Les notes de l'étudiant ont été mises à jour avec succès !" in captured.out

        # Vérifie que les notes de l'étudiant ont été correctement mises à jour
        student = self.view.student_controller.get_student_database_controller("John Doe")
        assert any(subject['name'] == "Math" and subject['grade'] == 16.0 for subject in student['lessons'])
        assert any(subject['name'] == "Science" and subject['grade'] == 12.0 for subject in student['lessons'])
        assert any(subject['name'] == "History" and subject['grade'] == 15.0 for subject in student['lessons'])

    @patch('builtins.input', side_effect=['15', '10', '10'])  # Ajoute les entrées simulées nécessaires
    @patch('views.student_menu_views.click.prompt')
    @patch('views.student_menu_views.click.confirm')
    def test_update_student_info_success(self, mock_confirm, mock_prompt, mock_input):
        # Prépare le mock pour simuler un étudiant existant
        mock_prompt.side_effect = [
            'John Doe',  # Nom de l'étudiant à mettre à jour
            'Johnny',    # Nouveau prénom
            'Doe',       # Nouveau nom (même que l'ancien)
            'Class A',   # Nouvelle classe (même que l'ancienne)
            'Math',      # Nouveau nom de matière
            '15',        # Nouvelle note pour Math
            'Science',   # Nouveau nom de matière
            '10',        # Nouvelle note pour Science
            'History'    # Nouveau nom de matière
        ]
        mock_confirm.return_value = True  # Confirme la mise à jour

        # Appel de la méthode à tester
        self.view.update_student_info()

        # Vérifie que l'étudiant a été mis à jour dans la base de données
        updated_student = self.view.student_controller.get_student_database_controller('Johnny Doe')
        assert updated_student['first_name'] == 'Johnny'
        assert updated_student['last_name'] == 'Doe'
        assert updated_student['classroom_name'] == 'Class A'
        assert len(updated_student['lessons']) == 3  # Vérifie que les leçons ont été mises à jour

    @patch('builtins.input', side_effect=['John Doe', '', '', '', 'Math', '', 'Science', '', 'History'])
    @patch('views.student_menu_views.click.confirm')
    @patch('views.student_menu_views.click.prompt', return_value='John Doe')  # Mock click.prompt ici
    def test_update_student_info_no_changes(self, mock_prompt, mock_confirm, mock_input):
        # Simule que la confirmation est vraie
        mock_confirm.return_value = True  

        # Prépare le mock pour simuler un étudiant existant
        self.view.student_controller.add_student_database_controller({
            'first_name': 'John',
            'last_name': 'Doe',
            'classroom_name': 'Class A',
            'lessons': [
                {'name': 'Math', 'grade': ''},
                {'name': 'Science', 'grade': ''},
                {'name': 'History', 'grade': ''},
            ]
        })

        # Appel de la méthode à tester
        self.view.update_student_info()

        # Vérifie que l'étudiant n'a pas été mis à jour
        updated_student = self.view.student_controller.get_student_database_controller('John Doe')
        assert updated_student['first_name'] == 'John'  # Doit conserver l'ancien prénom
        assert updated_student['last_name'] == 'Doe'    # Doit conserver l'ancien nom
        assert updated_student['classroom_name'] == 'Class A'  # Doit conserver l'ancienne classe
        assert len(updated_student['lessons']) == 3  # Vérifie que les leçons n'ont pas changé
