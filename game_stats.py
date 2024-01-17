class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

    def reset_stats(self):  # 游戏中可能变化的统计信息
        self.ship_left = self.ai_settings.ship_limit
