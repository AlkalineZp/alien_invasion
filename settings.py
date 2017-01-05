class Settings():
    # Класс для хранения всех настроек игры
    def __init__(self):
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        
        # Параметры корабля
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        
        # Параметры пули
        self.bullet_speed_factor = 10
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Настройки пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 50
        self.fleet_direction = 1 # 1 означает движение вправо а -1 в лево
