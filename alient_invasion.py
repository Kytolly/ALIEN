import pygame
from setting import Settings
from pygame.sprite import Group
from ship import Ships
import game_functions as gf
from alien import Alien


def run_game():
    # 元组(1200,800)初始化游戏，创建屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION")  # 设置标题
    ship = Ships(ai_settings, screen)
    alien = Alien(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    running = True
    while running:
        gf.check_events(ai_settings, screen, ship, bullets)  # 监视键盘和鼠标事件
        ship.update()
        gf.update_bullets(bullets)
        gf.update_aliens(ai_settings, aliens)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()
