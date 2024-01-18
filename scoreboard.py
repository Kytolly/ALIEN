import pygame.font


class ScoreBoard:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息用的字体
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分的图像
        self.score_image = None
        self.score_rect = None
        self.prep_score()

    def prep_score(self):
        score_str = str(self.stats.score)
        # 渲染图像
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        # 放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)


