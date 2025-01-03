import os
import random
import time

from openai import OpenAI

from core.config import CONFIG


class LLMOpenAI:
    def __init__(self):
        self.key = CONFIG.OPENAI.API_KEY
        self.client = OpenAI(api_key=self.key)

    def chat(self, model, messages):
        max_retries = 3
        for attempt in range(max_retries):
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
        raise Exception("Failed to get chat completion")
