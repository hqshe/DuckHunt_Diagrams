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



# Макет цілі, що використовується в тестах
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
