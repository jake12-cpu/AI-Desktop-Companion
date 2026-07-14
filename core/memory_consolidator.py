class MemoryConsolidator:


    def __init__(self, ai_client):

        self.ai_client = ai_client



    def consolidate(
        self,
        old_memory,
        new_memory
    ):


        prompt = [

            {
                "role":"system",
                "content":
                """
你负责整理用户长期记忆。

要求：
1. 保留用户事实
2. 合并重复信息
3. 生成一句简洁的长期记忆
4. 不要添加不存在的信息

只输出整理后的记忆内容。
"""
            },


            {
                "role":"user",
                "content":
                f"""
旧记忆：
{old_memory}


新信息：
{new_memory}


请合并：
"""
            }

        ]


        result = self.ai_client.chat(
            prompt
        )


        return result.strip()