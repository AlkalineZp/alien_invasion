import sys
import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button



def run_game():
    # Инициализирует игру и создает объект экрана
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Создание кнопки Play
    play_button = Button(ai_settings, screen, "Play")
    
    #Создание екземпляраа для хранения игровой статистики
    stats = GameStats(ai_settings)
    
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
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        # Обновление экрана
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, stars, play_button)
run_game()
