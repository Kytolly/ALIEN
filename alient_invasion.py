import pygame
from setting import Settings
from pygame.sprite import Group
from ship import Ships
import game_functions as gf
from alien import Alien
from game_stats import GameStats


def run_game():
    # 元组(1200,800)初始化游戏，创建屏幕对象
    pygame.init()
    ai_settings = Settings()
    # ai_settings.bullet_width = 1000
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION")  # 设置标题
    stats = GameStats(ai_settings)  # 存储游戏进行时的统计信息
    ship = Ships(ai_settings, screen)
    alien = Alien(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    running = True
    while running:
        gf.check_events(ai_settings, screen, ship, bullets)  # 监视键盘和鼠标事件
        ship.update()
        gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
        gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()
