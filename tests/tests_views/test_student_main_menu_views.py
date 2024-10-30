# tests/tests_views/test_student_main_menu_views.py
import pytest
import click
from rich.console import Console
from io import StringIO
from views.student_menu_views import StudentView


class TestStudentMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.student_menu = StudentView()
        # Mock de la méthode get_all_students_database_controller avant chaque test
        self.student_menu.student_controller.get_all_students_database_controller = lambda: [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'classroom_name': 'Class A',
                'grades': [12, 10, 15],  # Ajout des grades
                'lessons': ['Math', 'Science', 'History']  # Ajout des leçons
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'classroom_name': 'Class B',
                'grades': [9, 18, 19],  # Ajout des grades
                'lessons': ['English', 'Art', 'Physical Education']  # Ajout des leçons
            }
        ]

    def test_display_main_menu_show_students(self, mocker):
        # Simule l'entrée utilisateur pour sélectionner l'option d'affichage des étudiants
        mocker.patch('click.prompt', return_value='1') 

        # Mock print pour ignorer les impressions Rich
        mocker.patch.object(Console, 'print')

        # Appelle la méthode display_main_menu() de student_menu
        self.student_menu.display_main_menu()

        # Mock stdout pour capturer la sortie console
        mock_stdout = mocker.patch('sys.stdout', new_callable=StringIO)

        # Appelle la méthode display_students
        self.student_menu.display_students()

        # Capture la sortie console
        output = mock_stdout.getvalue()

        # Ajoute des assertions pour vérifier que les informations des étudiants sont affichées correctement
        assert "John Doe" in output
        assert "Class A" in output
        assert "Grades: 12, 10, 15" in output
        assert "Lessons: Math, Science, History" in output

        assert "Jane Smith" in output
        assert "Class B" in output
        assert "Grades: 9, 18, 19" in output
        assert "Lessons: English, Art, Physical Education" in output
