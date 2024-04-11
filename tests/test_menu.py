import pytest
import pygame
from Classes.Menu import Menu
from Classes.GameContext import GameContext


class MockSetting:
    def __init__(self, width=800, height=600, targets=None):
        if targets is None:
            targets = [[], [], []]
        self.width = width
        self.height = height
        self.targets = targets


@pytest.fixture
def mock_context():
    pygame.init()
    mock_settings = MockSetting(width=1024, height=768, targets=[[3, 4, 5], [3, 4, 5], [15, 12, 8, 3]])
    game_context = GameContext(mock_settings)
    return game_context


@pytest.fixture
def menu(mock_context):
    return Menu(mock_context)


def test_draw_game_over_switches_to_menu_on_menu_button_click(menu, mock_context, mocker):
    mocker.patch('pygame.mouse.get_pos', return_value=(475 + 130, 661 + 50))

    mocker.patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))

    mock_context.menu = False
    mock_context.game_over = True

    menu.draw_game_over()

    assert mock_context.menu is True
    assert mock_context.game_over is False


def test_draw_menu_switches_to_ammo_on_ammo_button_click(menu, mock_context, mocker):
    mock_context.menu = True
    mocker.patch('pygame.mouse.get_pos', return_value=(475 + 130, 524 + 50))
    mocker.patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))

    menu.draw_menu()

    assert mock_context.menu == False
    assert mock_context.mode == 1
    assert mock_context.level == 2
    assert mock_context.clicked == True
    assert mock_context.new_coords == True


def test_draw_menu_switches_to_freeplay_on_freeplay_button_click(menu, mock_context, mocker):
    mock_context.menu = True
    mocker.patch('pygame.mouse.get_pos', return_value=(170 + 130, 524 + 50))
    mocker.patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))

    menu.draw_menu()

    assert mock_context.menu == False
    assert mock_context.mode == 0
    assert mock_context.level == 1
    assert mock_context.clicked == True
    assert mock_context.new_coords == True


def test_draw_menu_switches_to_timed_on_timed_button_click(menu, mock_context, mocker):
    mock_context.menu = True
    mocker.patch('pygame.mouse.get_pos', return_value=(170 + 130, 660 + 50))
    mocker.patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))

    menu.draw_menu()

    assert mock_context.menu == False
    assert mock_context.mode == 2
    assert mock_context.level == 3
    assert mock_context.clicked == True
    assert mock_context.new_coords == True


def test_draw_pause_resumes_game_on_resume_button_click(menu, mock_context, mocker):
    mock_context.pause = True
    mocker.patch('pygame.mouse.get_pos', return_value=(200 + 130, 700 + 50))
    mocker.patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))

    menu.draw_pause()

    assert mock_context.pause == False
    assert mock_context.level == mock_context.resume_level
    assert mock_context.clicked == True
