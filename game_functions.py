import sys
import pygame
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    
        
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
          
                    
def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Обрабатывает нажатия клавиш и события мыши"""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, ship, bullets)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        
        aliens.empty()
        bullets.empty()
        
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
                
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, stars, play_button):
    """Обновляет изображения на экране"""
    
    screen.fill(ai_settings.bg_color)
    stars.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    # Отображение последнего прорисованого экрана
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Обновляет позиции пуль и удаляет старые пули"""
    
    bullets.update()
    
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)
   
   
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):    
    # Проверка попаданий в пришельцев
    # При попадании удалит пулю и пришельца.
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if len(aliens) == 0:
        #Уничтожение всех пуль и создание нового флота
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)  
            
            
def fire_bullet(ai_settings, screen, ship, bullets):
    # Создание новой пули и включение ее в группу bullets
    if len(bullets)< ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
        
def get_number_aliens_x(ai_settings, alien_width):
    """вычисление количества пришельцев в ряду."""
    
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    

def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов помещающихся на экране."""
    
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
        
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду"""
    
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
    
def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев"""    
    #Интервал между соседними пришельцами равен одной ширене пришельца.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # Создание пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
            
def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет его направление"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

    
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Обновляет позиции всех пришельцев"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
        # Проверка коллизий "пришелец-корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        #Проверка пришельцев добравшихся до низа экрана
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def get_number_stars_x(ai_settings, star_width):
    """вычисление количества звезд в ряду."""
    available_space_x = ai_settings.screen_width - 2 * star_width
    number_stars_x = int(available_space_x / (2 * star_width))
    return number_stars_x
    

def get_number_rows_star(ai_settings, star_height):
    """Определяет количество рядов помещающихся на экране."""
    available_space_y = (ai_settings.screen_height - (2 * star_height))
    number_rows = int(available_space_y / (2 * star_height))
    return number_rows
    
        
def create_star(ai_settings, screen, stars, stars_number, row_number):
    """Создает звезду и размещает ее в ряду"""
    star = Star(ai_settings, screen)
    random_x = randint(-10, 10)
    random_y = randint(-10, 10)
    star_width = star.rect.width
    star.x = (star_width + 4 * star_width * stars_number)+random_x
    star.rect.x = star.x
    star.rect.y = (star.rect.height + 4 * star.rect.height * row_number)+random_y
    stars.add(star)        
  
        
def create_stars(ai_settings, screen, stars):
    star = Star(ai_settings, screen)
    number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
    number_rows_star = get_number_rows_star(ai_settings, star.rect.height)
    
    # Создание звезд
    for row_number in range(number_rows_star):
        for stars_number in range(number_stars_x):
            create_star(ai_settings, screen, stars, stars_number, row_number)
    
    
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем"""
    if stats.ships_left > 0:
        # Уменьшает жизни корабля
        stats.ships_left -= 1
        
        # Очистка списков пуль и пришельцев.
        aliens.empty()
        bullets.empty()
        
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # Пауза.
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет добрался ли пришелец до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
