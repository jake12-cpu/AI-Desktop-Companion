class MemoryValidator:


    def validate(self, memory):

        content = memory.get(
            "content",
            ""
        )


        if not content:
            return False


        # 太短的不保存

        if len(content) < 4:
            return False


        # 这些属于普通聊天

        useless_words = [
            "你好",
            "哈哈",
            "谢谢",
            "好的",
            "嗯",
            "哦"
        ]


        for word in useless_words:

            if content == word:
                return False


        return True