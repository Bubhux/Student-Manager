# tests/tests_views/test_student_main_menu_views.py
import pytest
from unittest.mock import patch
from rich.console import Console
from views.student_menu_views import StudentView


class MockStudentDatabaseController:
    def __init__(self):
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
        return self.students

    def add_student_database_controller(self, student_data):
        self.students.append(student_data)  # Simuler l'ajout d'un étudiant


class TestStudentMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.student_view = StudentView()
        self.student_view.student_controller = MockStudentDatabaseController()
        self.console = Console()

    @patch('click.prompt', return_value='1')
    def test_display_students(self, mock_prompt, capsys):
        self.student_view.display_students()
        captured = capsys.readouterr()

        assert "Liste des étudiants triés par ordre alphabétique" in captured.out
        assert "John Doe" in captured.out
        assert "Jane Smith" in captured.out
        assert "Class A" in captured.out
        assert "Class B" in captured.out

    @patch('click.prompt', return_value='1')  # Simule la sélection de l'étudiant
    def test_display_student_informations(self, mock_prompt, capsys):
        self.student_view.display_student_informations(self.student_view.student_controller.get_all_students_database_controller())
        captured = capsys.readouterr()

        assert "Informations sur l'étudiant" in captured.out
        assert "Nom" in captured.out
        assert "John Doe" in captured.out
        assert "Matières et notes" in captured.out
        assert "Math" in captured.out
        assert "Science" in captured.out
        assert "History" in captured.out
        assert "Class A" in captured.out

    @patch('click.prompt', side_effect=['invalid_input'])
    def test_invalid_student_selection(self, mock_prompt, capsys):
        self.student_view.display_student_informations(self.student_view.student_controller.get_all_students_database_controller())
        captured = capsys.readouterr()

        assert "Aucun étudiant trouvé avec cette entrée." in captured.out

    @patch('click.prompt', side_effect=[
        'Alice',                  # Prénom
        'Johnson',                # Nom
        '2',                      # Nombre de matières
        'Math',                   # Nom de la première matière
        '15',                     # Note pour Math
        'Science',                # Nom de la deuxième matière
        '18',                     # Note pour Science
        'y'                       # Confirmation pour l'ajout
    ])
    @patch('builtins.input', side_effect=[
        'Alice',                  # Prénom
        'Johnson',                # Nom
        '2'                       # Nombre de matières
    ])
    @patch('rich.console.Console.print')
    @patch('click.confirm', return_value=True)  # Simuler la réponse de confirmation
    def test_add_student(self, mock_confirm, mock_print, mock_input, mock_prompt):
        # Simulation de l'ajout d'un étudiant
        self.student_view.add_student()

        # Vérifier que les bonnes informations sont affichées
        mock_print.assert_any_call("[bold cyan]Résumé des informations saisies :[/bold cyan]")
        mock_print.assert_any_call("[bold green]L'étudiant a été ajouté avec succès ![/bold green]")
        
        # Vérifier que l'étudiant a bien été ajouté à la base de données
        students = self.student_view.student_controller.get_all_students_database_controller()
        assert any(student['first_name'] == 'Alice' and student['last_name'] == 'Johnson' for student in students)

