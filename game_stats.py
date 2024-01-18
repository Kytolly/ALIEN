import json
import os

class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.game_active = False
        self.high_score = self.prep_history()  # 最高得分
        self.reset_stats()

    def reset_stats(self):  # 游戏中可能变化的统计信息
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def prep_history(self):
        data = "data.json"  # 加载历史数据
        if not os.path.exists(data):
            with open(data, 'w') as db:
                json.dump(0, db)  # 若data.json不存在，创建它
            history = 0
        else:
            with open(data) as db:
                history = json.load(db)
        return history