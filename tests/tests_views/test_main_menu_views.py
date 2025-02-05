# tests/tests_views/test_main_menu_views.py
import pytest
from unittest.mock import MagicMock
from views.main_menu_views import MainMenuView
from rich.console import Console


class TestMainMenuView:

    @pytest.fixture(autouse=True)
    def setup(self):
        """Fixture qui crée une instance de MainMenuView."""
        mock_db = MagicMock()  # Mock de la base de données
        self.main_menu = MainMenuView(mock_db)

    def test_display_main_menu_student_choice(self, mocker):
        """
        Teste le choix '1' dans le menu principal pour s'assurer que la méthode
        display_main_menu() de StudentView est appelée.
        """
        # Simule l'entrée utilisateur pour sélectionner "1" puis "q" pour quitter
        mocker.patch('click.prompt', side_effect=["1", "q"])

        # Mock de la méthode display_main_menu() de StudentView
        mock_student_view = mocker.patch.object(self.main_menu.student_view, 'display_main_menu')

        # Mock print pour ignorer les impressions Rich
        mocker.patch.object(Console, 'print')

        # Appelle la méthode display_main_menu()
        self.main_menu.display_main_menu()

        # Vérifie que display_main_menu() de StudentView est bien appelé
        mock_student_view.assert_called_once()

    def test_display_main_menu_classroom_choice(self, mocker):
        """
        Teste le choix '2' dans le menu principal pour s'assurer que la méthode
        display_main_menu() de ClassroomView est appelée.
        """
        # Simule l'entrée utilisateur pour sélectionner "2" puis "q" pour quitter
        mocker.patch('click.prompt', side_effect=["2", "q"])

        # Mock de la méthode display_main_menu() de ClassroomView
        mock_classroom_view = mocker.patch.object(self.main_menu.classroom_view, 'display_main_menu')

        # Mock print pour ignorer les impressions Rich
        mocker.patch.object(Console, 'print')

        # Appelle la méthode display_main_menu()
        self.main_menu.display_main_menu()

        # Vérifie que display_main_menu() de ClassroomView est bien appelé
        mock_classroom_view.assert_called_once()

    def test_display_main_menu_quit_choice(self, mocker):
        """
        Teste le choix 'q' pour s'assurer que le programme se termine correctement.
        """
        # Simule l'entrée utilisateur pour sélectionner "q"
        mocker.patch('click.prompt', return_value="q")

        # Mock print pour capturer le message de sortie
        mock_console_print = mocker.patch.object(Console, 'print')

        # Appelle la méthode display_main_menu()
        self.main_menu.display_main_menu()

        # Vérifie que le message de sortie est bien affiché
        mock_console_print.assert_any_call("Merci d'avoir utilisé Student Manager !")

    def test_display_main_menu_invalid_choice(self, mocker):
        """
        Teste une saisie invalide pour vérifier que le message d'erreur s'affiche.
        """
        # Simule l'entrée utilisateur pour un choix invalide puis "q" pour quitter
        mocker.patch('click.prompt', side_effect=["invalid_choice", "q"])

        # Mock print pour capturer les messages de console
        mock_console_print = mocker.patch.object(Console, 'print')

        # Appelle la méthode display_main_menu()
        self.main_menu.display_main_menu()

        # Vérifie que le message d'erreur s'affiche
        mock_console_print.assert_any_call(
            "Choix invalide, saisissez un nombre entre 1 et 2 ou q pour quitter l'application.",
            style="bold red"
        )
