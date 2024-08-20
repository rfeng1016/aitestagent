import os
import json
import dashscope
from prompt import user_prompt
from dashscope.api_entities.dashscope_response import Message


class ModelProvider(object):
    def __init__(self):
        self.api_key = os.environ.get('DASH_SCOPE_API_KEY')
        self.model_name = os.environ.get('MODEL_NAME')
        self._client = dashscope.Generation()
        self.max_retry_time = 3

    def chat(self, prompt, chat_history):
        cur_retry_time = 0
        while cur_retry_time < self.max_retry_time:
            cur_retry_time += 1
            try:
                messages = [
                    Message(role="system", content=prompt)
                ]
                for his in chat_history:
                    messages.append(Message(role="user", content=his[0]))
                    messages.append(Message(role="system", content=his[1]))
                messages.append(Message(role="user", content=user_prompt))

                response = self._client.call(
                    model=self.model_name,
                    api_key=self.api_key,
                    messages=messages
                )
                content = json.loads(response["output"]["text"])
                return content
            except Exception as e:
                print(f"call llm exception: {e}")
        return {}