import json
import random
import copy


class MessageManager:

    def __init__(self, character_manager):

        self.character_manager = character_manager

        config = character_manager.config

        self.messages = [

            {
                "role": "system",
                "content": config.get(
                    "system_prompt",
                    ""
                )
            }

        ]

        idle_path = (
            character_manager.get_character_path()
            + "/idle_messages.json"
        )

        try:

            with open(
                idle_path,
                "r",
                encoding="utf-8"
            ) as f:
                self.idle_messages = json.load(f)

        except FileNotFoundError:

            self.idle_messages = []


    def add_user_message(self, text):

        self.messages.append(
            {
                "role": "user",
                "content": text
            }
        )


    def add_assistant_message(self, text):

        self.messages.append(
            {
                "role": "assistant",
                "content": text
            }
        )

    def get_messages(self):

        return copy.deepcopy(
            self.messages
        )

    def get_memory_context(self, memories):

        if not memories:
            return None

        memory_text = "\n".join(
            [
                f"- {memory['content']}"
                for memory in memories
            ]
        )

        return {
            "role": "system",
            "content":
                "用户长期记忆:\n"
                + memory_text
        }

    def get_random_idle_message(self):

        if not self.idle_messages:
            return ""

        return random.choice(
            self.idle_messages
        )