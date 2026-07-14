import json
import os
from datetime import datetime


class MemoryManager:


    def __init__(self):

        self.path = "memory/memory.json"

        self.memories = []

        self.load()



    def load(self):

        folder = "memory"

        if not os.path.exists(folder):

            os.makedirs(folder)


        if not os.path.exists(self.path):

            self.save()


        else:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as f:

                self.memories = json.load(f)



    def save(self):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.memories,
                f,
                ensure_ascii=False,
                indent=4
            )

    def add_memory(self, memory):

        content = memory["content"]

        memory_type = memory.get(
            "type",
            "fact"
        )

        importance = memory.get(
            "importance",
            0.5
        )

        # 去重检查
        for old_memory in self.memories:

            if old_memory["content"] == content:
                return

        new_memory = {

            "type": memory_type,

            "content": content,

            "importance": importance,

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }

        self.memories.append(
            new_memory
        )

        self.save()


    def get_memories(self):

        return self.memories

    def build_memory_prompt(self, query=None):

        if query:

            memories = self.search_memory(query)

        else:

            memories = self.memories

        if not memories:
            return ""

        text = "关于旅行者的信息：\n"

        for memory in memories:
            text += (
                f"- {memory['content']}\n"
            )

        return text

    def search_memory(self, query):

        if not self.memories:
            return []

        stop_words = [
            "我",
            "你",
            "的",
            "是",
            "了",
            "吗",
            "什么",
            "怎么",
            "一下",
            "一下子",
            "还"
        ]

        keywords = [
            char
            for char in query
            if char not in stop_words
        ]

        results = []

        for memory in self.memories:

            content = memory["content"]

            score = 0

            for keyword in keywords:

                if keyword in content:
                    score += 1

            if score >= 2:
                results.append(
                    memory
                )

        return results