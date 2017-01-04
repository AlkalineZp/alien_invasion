import sys
import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group



def run_game():
    # Инициализирует игру и создает объект экрана
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Создание корабля
    ship = Ship(ai_settings, screen)
    
    # Создание группы для хранения пуль.
    bullets = Group()
    aliens = Group()
    stars = Group()
    
    # Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # Создание звездного неба
    gf.create_stars(ai_settings, screen, stars)
    
    
    # Запуск игрового цикла
    while True:
        # Отслеживание событий клавиатуры и миши
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
        gf.update_aliens(ai_settings, aliens)
        # Обновление экрана
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stars)
run_game()
