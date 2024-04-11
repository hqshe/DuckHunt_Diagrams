import pygame
import pytest
from Classes.GameContext import GameContext


class MockSettings:
    def __init__(self, width=800, height=600, targets=[[], [], []]):
        self.width = width
        self.height = height
        self.targets = targets


@pytest.fixture
def mock_game_context():
    pygame.init()
    mock_settings = MockSettings(width=1024, height=768, targets=[[3, 4, 5], [3, 4, 5], [15, 12, 8, 3]])
    game_context = GameContext(mock_settings)
    return game_context


def test_pygame_init(mock_game_context):
    assert pygame.get_init()


def test_init(mock_game_context):
    settings = mock_game_context.settings
    assert mock_game_context.WIDTH == settings.width
    assert mock_game_context.HEIGHT == settings.height
    assert mock_game_context.targets == settings.targets


def test_generate_enemy_coordinates(mock_game_context):
    mock_game_context.generate_enemy_coordinates()
    assert len(mock_game_context.one_coords) == 3
    assert len(mock_game_context.two_coords) == 3
    assert len(mock_game_context.three_coords) == 4


@pytest.mark.parametrize("level", [1, 2, 3])
def test_draw_level(mock_game_context, level):
    coords = mock_game_context.one_coords if level == 1 else mock_game_context.two_coords if level == 2 else mock_game_context.three_coords
    mock_game_context.level = level
    target_rects = mock_game_context.draw_level(coords)
    assert len(target_rects) == 3 if level < 3 else 4
    for i in range(3 if level < 3 else 4):
        assert len(target_rects[i]) == len(coords[i])


def test_draw_score(mock_game_context):
    mock_game_context.draw_score()


@pytest.mark.parametrize("level, initial_coords, expected_coords", [
    (1, [[(100, 200), (300, 400), (500, 600)], [(100, 200), (300, 400), (500, 600)], [(100, 200), (300, 400), (500, 600)]], [[(99, 200), (299, 400), (499, 600)], [(98, 200), (298, 400), (498, 600)], [(96, 200), (296, 400), (496, 600)]]),
    (2, [[(100, 200), (300, 400), (500, 600)], [(100, 200), (300, 400), (500, 600)], [(100, 200), (300, 400), (500, 600)]], [[(99, 200), (299, 400), (499, 600)], [(98, 200), (298, 400), (498, 600)], [(96, 200), (296, 400), (496, 600)]]),
    (3, [[(100, 200), (300, 400), (500, 600)], [(100, 200), (300, 400), (500, 600)], [(100, 200), (300, 400), (500, 600)], [(100, 200), (300, 400), (500, 600)]], [[(99, 200), (299, 400), (499, 600)], [(98, 200), (298, 400), (498, 600)], [(96, 200), (296, 400), (496, 600)], [(92, 200), (292, 400), (492, 600)]])
])
def test_move_level(mock_game_context, level, initial_coords, expected_coords):
    mock_game_context.level = level
    if level == 1:
        mock_game_context.one_coords = initial_coords
    elif level == 2:
        mock_game_context.two_coords = initial_coords
    elif level == 3:
        mock_game_context.three_coords = initial_coords

    new_coords = mock_game_context.move_level()

    assert new_coords == expected_coords
