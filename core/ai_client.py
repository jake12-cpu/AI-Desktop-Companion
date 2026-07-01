import json
from openai import OpenAI


class AIClient:

    def __init__(self):

        with open("config/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        self.client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )

        self.model = config["model"]
        print("读取配置成功！")
        print(config["base_url"])
        print(self.model)

    def chat(self, message):
        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]

        )

        return response.choices[0].message.content

