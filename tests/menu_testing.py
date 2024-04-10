import pytest
from unittest.mock import MagicMock
import pygame
from Classes.Menu import Menu

@pytest.fixture
def mock_context():
    context = MagicMock()
    context.game_over_img = MagicMock()
    context.big_font = MagicMock()
    context.big_font.render = MagicMock(return_value=MagicMock())
    context.screen = MagicMock()
    context.clicked = False
    context.mode = 0
    context.time_passed = 100
    context.points = 200
    pygame.mouse.get_pos = MagicMock(return_value=(0, 0))
    pygame.mouse.get_pressed = MagicMock(return_value=(True, False, False))
    pygame.rect.Rect = MagicMock(return_value=MagicMock())
    return context

@pytest.fixture
def menu(mock_context):
    return Menu(mock_context)

def test_draw_game_over_switches_to_menu_on_menu_button_click(menu, mock_context):
    mock_context.menu = False
    mock_context.game_over = True
    pygame.mouse.get_pos.return_value = (500, 700)

    menu.draw_game_over()

    assert mock_context.menu == True
    assert mock_context.game_over == False
    assert mock_context.clicked == True
def test_draw_menu_switches_to_freeplay_on_freeplay_button_click(menu, mock_context):
    mock_context.menu = True
    pygame.mouse.get_pos.return_value = (200, 550)

    menu.draw_menu()

    assert mock_context.menu == False
    assert mock_context.mode == 0
    assert mock_context.level == 1
    assert mock_context.clicked == True
    assert mock_context.new_coords == True

def test_draw_pause_resumes_game_on_resume_button_click(menu, mock_context):
    mock_context.pause = True
    pygame.mouse.get_pos.return_value = (200, 700)

    menu.draw_pause()

    assert mock_context.pause == False
    assert mock_context.level == mock_context.resume_level
    assert mock_context.clicked == True