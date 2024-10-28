# tests/tests_views/test_student_main_menu_views.py
import pytest
from views.student_menu_views import StudentView
from rich.console import Console


class TestStudentMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self):
        """Fixture qui crée une instance de StudentView."""
        self.student_menu = StudentView()
