class MemoryExtractor:


    def __init__(self):
        pass



    def extract(self, text):

        memories = []


        # =================
        # 偏好类
        # =================

        preference_words = [
            "喜欢",
            "爱吃",
            "喜欢玩",
            "喜欢看",
            "爱玩"
        ]


        if any(
            word in text
            for word in preference_words
        ):

            memories.append(
                {
                    "type": "preference",
                    "content": text,
                    "importance": 0.7
                }
            )



        # =================
        # 个人事实
        # =================

        fact_words = [
            "我是",
            "我的",
            "我有",
            "我用",
            "我叫"
        ]


        if any(
            word in text
            for word in fact_words
        ):

            memories.append(
                {
                    "type": "fact",
                    "content": self.clean_content(text),
                    "importance": 0.9
                }
            )



        return memories



    def clean_content(self, text):

        text = text.strip()

        return text