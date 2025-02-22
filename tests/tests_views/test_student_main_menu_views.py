# tests/tests_views/test_student_main_menu_views.py
import pytest
import mongomock
from unittest.mock import patch, MagicMock
from rich.console import Console
from views.student_menu_views import StudentView
import re


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

        self.db = {
            "students": self.students,
            "classrooms": [
                {"name": "Class A", "number_of_places_available": 10, "number_of_students": []},
                {"name": "Class B", "number_of_places_available": 5, "number_of_students": []}
            ]
        }

    def __getitem__(self, item):
        if item == 'students':
            return self.students
        elif item == 'classrooms':
            return []
        raise KeyError(f"Collection '{item}' non trouvée.")

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

    def delete_student_database_controller(self, student_name):
        # Simule la suppression d'un étudiant en le retirant de la liste
        for index, student in enumerate(self.students):
            full_name = f"{student['first_name']} {student['last_name']}"
            if student_name == full_name or student_name == student['first_name']:
                del self.students[index]  # Retire l'étudiant de la liste
                break

    def calculate_student_average_database_controller(self, student_name):
        student = self.get_student_database_controller(student_name)
        if student and student.get('grades'):  # Vérifie que les notes existent
            return sum(student['grades']) / len(student['grades'])  # Retourne une moyenne correcte
        return None  # Retourne None si aucun étudiant ou aucune


# Classe de test pour les vues du menu principal des étudiants
class TestStudentMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self, mock_mongo_db):
         # Simule une base de données MongoDB avec mongomock
        self.mock_db = mongomock.MongoClient()['test_database']

        # Injecte la base de données fictive dans StudentView
        self.view = StudentView(self.mock_db)
        self.view.student_controller = MockStudentDatabaseController()
        self.console = Console()

        # Patching dans setup
        self.mock_classroom_patch = patch('controllers.classroom_controller.ClassroomDatabaseController.get_classroom_database_controller',
                                          return_value={"name": "Wonderland", "number_of_places_available": 10, "number_of_students": []})
        self.mock_classroom = self.mock_classroom_patch.start()

    def teardown(self):
        # Arrête le patch après chaque test
        self.mock_classroom_patch.stop()

    def clean_output(self, output):
        return re.sub(r'\x1b\[[0-9;]*m', '', output)  # Supprime les codes d'échappement ANSI

    def remove_ansi_sequences(self, text):
        ansi_escape = re.compile(r'\x1b\[([0-9]+)(;[0-9]+)*m')
        return ansi_escape.sub('', text)

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
        self.mock_classroom.assert_called()

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
        mock_prompt.side_effect = [
            "John Doe",  # Nom de l'étudiant
            "16",        # Nouvelle note pour Math
            "12",        # Nouvelle note pour Science
            "15"         # Nouvelle note pour History
        ]

        mock_confirm.return_value = True

        self.view.update_student_grades()

        captured = capsys.readouterr()

        print(captured.out)  # Pour voir la sortie capturée

        # Enlève les codes d'échappement ANSI avant d'affirmer
        assert "Notes modifiées" in captured.out
        assert "Nouvelle note de Math : 16.0" in self.clean_output(captured.out)
        assert "Nouvelle note de Science : 12.0" in self.clean_output(captured.out)
        assert "Nouvelle note de History : 15.0" in self.clean_output(captured.out) 
        assert "Les notes de l'étudiant ont été mises à jour avec succès !" in self.clean_output(captured.out)

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
    @patch('views.student_menu_views.click.prompt', return_value='John Doe')
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

    @patch('views.student_menu_views.click.prompt')
    def test_update_student_info_student_not_found(self, mock_prompt):
        # Prépare le mock pour simuler la tentative de mise à jour d'un étudiant qui n'existe pas
        mock_prompt.return_value = 'Non Existant Student'  # Nom de l'étudiant qui n'existe pas

        # Capture les sorties de la console
        with patch('rich.console.Console.print') as mock_print:
            self.view.update_student_info()
            mock_print.assert_called_with("Aucun étudiant trouvé avec le nom [bold]Non Existant Student[/bold]. Vérifiez le nom de l'étudiant.", style="bold red")

    @patch('views.student_menu_views.click.prompt')
    @patch('views.student_menu_views.click.confirm')
    def test_delete_student_success(self, mock_confirm, mock_prompt, capsys):
        mock_prompt.return_value = '1'  # Sélectionne 'Jane Smith'
        mock_confirm.return_value = True

        # Appelle la méthode
        self.view.delete_student()

        # Nettoie les séquences ANSI des appels réels
        actual_calls = [self.remove_ansi_sequences(str(call)) for call in mock_confirm.call_args_list]

        # Vérifie que le message attendu est dans les appels réels
        expected_message = "Êtes-vous sûr de vouloir supprimer l'étudiant 'Jane Smith' ?"
        assert any(expected_message in call for call in actual_calls)

    @patch('views.student_menu_views.click.prompt')
    @patch('views.student_menu_views.StudentDatabaseController.delete_student_database_controller')
    def test_delete_student_cancel(self, mock_delete, mock_prompt):
        # Simule une entrée utilisateur pour sélectionner un étudiant
        mock_prompt.return_value = '1'  # Simule la sélection de l'étudiant à supprimer

        # Teste la suppression d'un étudiant mais avec annulation
        mock_delete.return_value = None  # La suppression ne doit pas réellement se produire

        # Capture la sortie console pendant l'exécution de la fonction
        with patch('rich.console.Console.print') as mock_print, patch('click.confirm') as mock_confirm:
            mock_confirm.return_value = False  # Simule l'annulation de la suppression

            # Appel à la fonction de suppression d'un étudiant
            self.view.delete_student()

            # Vérifie que la suppression a bien été annulée
            mock_print.assert_any_call("Suppression annulée.", style="bold red")

            # Vérifie que la méthode delete_student_database_controller n'a pas été appelée
            mock_delete.assert_not_called()

    def test_no_students_to_delete(self):
        # Teste l'absence d'étudiants à supprimer
        self.view.student_controller.students = []  # Vide la liste des étudiants

        with patch('rich.console.Console.print') as mock_print:
            self.view.delete_student()

            # Vérifie que le message "Il n'y a pas d'étudiants disponibles" est affiché
            mock_print.assert_any_call("Il n'y a pas d'étudiants disponibles.", style="bold red")

    @patch('views.student_menu_views.click.prompt')
    @patch('views.student_menu_views.StudentDatabaseController.calculate_student_average_database_controller')
    def test_calculate_student_average(self, MockStudentController, mock_prompt, capsys):

        mock_student_controller = MockStudentController.return_value
        mock_student_controller.calculate_student_average_database_controller.return_value = 15.33 

        mock_prompt.side_effect = ['1']

        self.view.calculate_student_average()

        captured = capsys.readouterr()
        assert "Moyenne de l'étudiant Jane Smith : 15.33" in captured.out


# Classe de test pour les vues du menu principal des étudiants
class TestStudentMainMenuViewChoice:

    @pytest.fixture(autouse=True)
    def setup(self):
        """Fixture qui crée une instance de StudentView."""
        self.mock_db = MockStudentDatabaseController()
        self.student_main_menu = StudentView(db=self.mock_db)

    def test_display_student_choice(self, mocker):
        mocker.patch('click.prompt', side_effect=["1", "r"])
        mock_student_menu_view = mocker.patch.object(self.student_main_menu, 'display_students')
        mocker.patch.object(Console, 'print')

        self.student_main_menu.display_main_menu()
        mock_student_menu_view.assert_called_once()

    def test_add_student_choice(self, mocker):
        mocker.patch('click.prompt', side_effect=["2", "r"]) 
        mock_add_student = mocker.patch.object(self.student_main_menu, 'add_student')
        mocker.patch.object(Console, 'print')

        self.student_main_menu.display_main_menu()
        mock_add_student.assert_called_once()

    def test_add_subject_to_student_choice(self, mocker):
        mocker.patch('click.prompt', side_effect=["3", "r"]) 
        mock_add_subject = mocker.patch.object(self.student_main_menu, 'add_subject_to_student') 
        mocker.patch.object(Console, 'print')

        self.student_main_menu.display_main_menu()
        mock_add_subject.assert_called_once()

    def test_update_student_grades_choice(self, mocker):
        mocker.patch('click.prompt', side_effect=["4", "r"])
        mock_update_grades = mocker.patch.object(self.student_main_menu, 'update_student_grades')
        mocker.patch.object(Console, 'print')

        self.student_main_menu.display_main_menu()
        mock_update_grades.assert_called_once()

    def test_update_student_info_choice(self, mocker):
        mocker.patch('click.prompt', side_effect=["5", "r"]) 
        mock_update_info = mocker.patch.object(self.student_main_menu, 'update_student_info')
        mocker.patch.object(Console, 'print')

        self.student_main_menu.display_main_menu()
        mock_update_info.assert_called_once()

    def test_calculate_student_average_choice(self, mocker):
        mocker.patch('click.prompt', side_effect=["6", "r"])
        mock_calculate_average = mocker.patch.object(self.student_main_menu, 'calculate_student_average')
        mocker.patch.object(Console, 'print')

        self.student_main_menu.display_main_menu()
        mock_calculate_average.assert_called_once()

    def test_delete_student_choice(self, mocker):
        mocker.patch('click.prompt', side_effect=["7", "r"])
        mock_delete_student = mocker.patch.object(self.student_main_menu, 'delete_student')
        mocker.patch.object(Console, 'print')

        self.student_main_menu.display_main_menu()
        mock_delete_student.assert_called_once()

    def test_return_to_main_menu_choice(self, mocker):
        mocker.patch('click.prompt', side_effect=["r"]) 
        mocker.patch.object(Console, 'print')

        self.student_main_menu.display_main_menu()
        Console.print.assert_called_with("Menu principal !")
