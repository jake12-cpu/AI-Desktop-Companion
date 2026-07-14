import json
import os
from datetime import datetime


class MemoryManager:

    def __init__(
            self,
            consolidator=None
    ):

        self.consolidator = consolidator

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

    def similarity(self, text1, text2):

        words1 = set(text1)
        words2 = set(text2)

        if not words1 or not words2:
            return 0

        return len(
            words1 & words2
        ) / len(
            words1 | words2
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

            sim = self.similarity(
                old_memory["content"],
                content
            )

            if sim > 0.5:

                if self.consolidator:
                    summary = self.consolidator.consolidate(

                        old_memory["content"],

                        content

                    )

                    old_memory["content"] = summary

                old_memory["importance"] += 0.1

                old_memory["used_count"] += 1

                self.save()

                return

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        new_memory = {

            "type": memory_type,

            "content": content,

            "importance": importance,

            "base_importance": importance,

            "created_time": now,

            "last_used": now,

            "used_count": 0

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
                f"- {memory['content']}"
                f"(重要程度:{memory.get('importance', 0.5)})\n"
            )

        return text

    def search_memory(self, query):

        if not self.memories:
            return []
        self.update_memory_importance()

        stop_words = [
            "我",
            "你",
            "的",
            "是",
            "吗",
            "什么",
            "怎么",
            "还",
            "记得"
        ]

        keywords = [
            word
            for word in query
            if word not in stop_words
        ]

        results = []

        for memory in self.memories:

            content = memory["content"]

            score = 0
            # 类型权重

            if memory.get("type") == "preference":

                if "喜欢" in query or "吃" in query:
                    score += 3

            if memory.get("type") == "fact":

                if "电脑" in query or "用" in query:
                    score += 3

            # 1.关键词匹配
            for keyword in keywords:

                if keyword in content:
                    score += 1

            # 强关键词

            strong_keywords = [
                "吃",
                "电脑",
                "专业",
                "学校",
                "工作",
                "住",
                "喜欢玩"
            ]

            for word in strong_keywords:

                if word in query and word in content:
                    score += 3

            # 2.重要程度加权

            score += (
                memory.get(
                    "importance",
                    0.5
                )
            )

            if (
                    score > 2
                    and memory.get(
                "importance",
                0.5
            ) >= 0.3
            ):
                self.update_memory_usage(
                    memory
                )

                memory_copy = memory.copy()

                memory_copy["score"] = score

                results.append(
                    memory_copy
                )

        # 按分数排序

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:3]

    def update_memory_usage(self, memory):

        for item in self.memories:

            if item["content"] == memory["content"]:
                item["last_used"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                item["used_count"] = (
                        item.get(
                            "used_count",
                            0
                        )
                        + 1
                )

                self.save()

                break

    def update_memory(self, old_content, new_content):

        for memory in self.memories:

            if memory["content"] == old_content:
                memory["content"] = new_content

                self.save()

                return True

        return False

    def update_memory_importance(self):

        now = datetime.now()

        for memory in self.memories:
            base = memory.get(
                "base_importance",
                memory.get(
                    "importance",
                    0.5
                )
            )

            # 使用次数奖励

            used_count = memory.get(
                "used_count",
                0
            )

            usage_bonus = min(
                used_count * 0.02,
                0.3
            )

            # 时间衰减

            last_used = datetime.strptime(
                memory.get(
                    "last_used"
                ),
                "%Y-%m-%d %H:%M:%S"
            )

            days = (
                    now - last_used
            ).days

            decay = days * 0.01

            importance = (
                    base
                    + usage_bonus
                    - decay
            )

            # 限制范围

            importance = max(
                0.1,
                min(
                    importance,
                    1
                )
            )

            memory["importance"] = round(
                importance,
                2
            )

        self.save()
    def delete_memory(self, content):

        for memory in self.memories:

            if memory["content"] == content:

                self.memories.remove(
                    memory
                )

                self.save()

                return True

        return False