import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载alien
        self.image = pygame.image.load('img/alien.bmp')
        self.rect = self.image.get_rect()

        # alien的初始位置是左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        # 绘制alien
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 向右移动外星人
        self.x += self.ai_settings.alien_speed_factor
        self.rect.x = self.x
