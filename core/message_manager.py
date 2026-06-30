import random


class MessageManager:

    def __init__(self):
        self.messages = [
            "你好，旅行者！",
            "今天学习了吗？",
            "加油，我陪着你！",
            "不要忘记喝水哦~",
            "派蒙一直陪着你！"
        ]

    def random_message(self):
        return random.choice(self.messages)