import os
import time
import random
from openai import OpenAI

from core.config import CONFIG


class LLMOpenAI:
    def __init__(self):
        self.key = CONFIG.OPENAI.API_KEY
        self.client = OpenAI(api_key=self.key)

    def chat(self, model, messages):
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                timeout=120,
            )
            return completion
        except Exception as ex:
            print(f"[CHAT COMPLETION] {ex}")
            time.sleep(random.randint(10, 20))
            return self.chat(model, messages)
