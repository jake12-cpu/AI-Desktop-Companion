from openai import OpenAI


class AIClient:

    def __init__(self, config_manager):

        self.config_manager = config_manager

        self.api_key = config_manager.get(
            "api_key"
        )

        self.base_url = config_manager.get(
            "base_url"
        )

        self.model = config_manager.get(
            "model"
        )

        if self.api_key:

            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

        else:

            self.client = None
        self.config_manager.config_changed.connect(
            self.update_config
        )
        print("读取配置成功！")
        print(self.base_url)
        print(self.model)

    def update_config(self, key, value):

        if key == "api_key":

            self.api_key = value


        elif key == "base_url":

            self.base_url = value

            if self.api_key:

                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )

            else:

                self.client = None


        elif key == "model":

            self.model = value

    def chat(self, messages):

        if self.client is None:
            return "旅行者，请先在设置中填写API Key哦~"

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=messages

            )

            return response.choices[0].message.content


        except Exception as e:

            print(
                "AI请求失败:",
                e
            )

            return "派蒙暂时连接不上服务器了，请检查模型配置哦！"