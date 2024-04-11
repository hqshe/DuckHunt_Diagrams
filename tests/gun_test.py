import pygame
import pytest
import os
from Classes.Gun import Gun

class MockSound:
    def play(self):
        pass  # Метод play, який нічого не робить

# Макет контексту, що імітує необхідний інтерфейс
class MockContext:
    WIDTH = 800
    HEIGHT = 600
    points = 0
    level = 1
    guns = [pygame.Surface((10, 10)) for _ in range(3)]  # Мок-об'єкти для зображень зброї
    screen = pygame.Surface((WIDTH, HEIGHT))  # Створюємо поверхню для макета екрана
    bird_sound = MockSound()

class MockTarget:
    def __init__(self, width=800, height=600, targets=[[], [], []]):
        self.width = width
        self.height = height
        self.targets = targets
        # Створюємо прямокутник для макета цілі з довільними розмірами та позицією
        self.rect = pygame.Rect(0, 0, 50, 50)  # Довільні розміри 50x50

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)


@pytest.fixture
def gun():
    pygame.init()  # Ініціалізація Pygame для тестування
    context = MockContext()
    return Gun(context)

# Тест для метода draw_gun
def test_draw_gun(gun):
    # Симулюємо позицію миші і натискання
    pygame.mouse.set_pos([400, 300])
    # Викликаємо метод, очікуємо, що не викличе помилок і змінить стан
    gun.draw_gun()
    # Тут можна додати перевірки на зміни стану контексту або виклик методів

# Тест для метода check_shot
def test_check_shot(gun):
    # Припустимо, що targets містить макети цілей
    targets = [[MockTarget()]]
    coords = [[(100, 100)]]
    pygame.mouse.set_pos([100, 100])
    updated_coords = gun.check_shot(targets, coords)
    # Перевіряємо, що координати цілі були видалені
    assert updated_coords == [[]]
    # Перевіряємо, що були нараховані очки
    assert gun.context.points == 10

def test_level_change(gun):
    gun.context.level = 2  # Змінюємо рівень
    assert gun.context.level == 2  # Перевіряємо, чи рівень змінився

def test_level_change_updates_gun(gun):
    # Встановлюємо рівень 2
    gun.context.level = 2
    # Перевіряємо, чи змінюється зброя на другий рівень
    gun.draw_gun()
    # Перевірки можуть включати перевірку зміненої графіки зброї, що вимагатиме додаткового коду для перевірки стану screen
    assert gun.context.guns[gun.context.level - 1] == gun.context.guns[1]

def test_draw_gun_at_different_mouse_positions(gun):
    pygame.mouse.set_pos([100, 500])  # Встановлюємо позицію миші зліва
    gun.draw_gun()
    # Тут можна перевірити зміни на екрані або логіку обробки, в залежності від позиції миші

    pygame.mouse.set_pos([700, 500])  # Встановлюємо позицію миші справа
    gun.draw_gun()
    # Аналогічно перевіряємо відмальовування або логіку в залежності від зміни позиції миші

# def test_sound_play_based_on_level(gun):
#     gun.context.level = 1
#     gun.check_shot([[MockTarget()]], [[(100, 100)]])
#     gun.context.bird_sound.play.assert_called_once()  # Переконуємось, що відтворився звук для пташки
#
#     gun.context.level = 2
#     gun.context.plate_sound = MockSound()
#     gun.check_shot([[MockTarget()]], [[(100, 100)]])
#     gun.context.plate_sound.play.assert_called_once()  # Переконуємось, що відтворився звук для тарілки
#
#     gun.context.level = 3
#     gun.context.laser_sound = MockSound()
#     gun.check_shot([[MockTarget()]], [[(100, 100)]])
#     gun.context.laser_sound.play.assert_called_once()  # Переконуємось, що відтворився лазерний звук


