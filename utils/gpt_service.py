import base64
from io import BytesIO
import openai
import os

token = os.getenv('TOKEN_OPENAI')
token = 'sk-proj-' + token[:3:-1] if token.startswith('gpt:') else token
openai.api_key = token


class ChatGPTService:
    def __init__(self):
        self.message_history = []

    def set_system_message(self, content):
        self.message_history.append({"role": "system", "content": content})

    def add_user_message(self, user_content):
        self.message_history.append({"role": "user", "content": user_content})

    def add_assistant_message(self, content):
        self.message_history.append({"role": "assistant", "content": content})

    def get_response(self, model='gpt-3.5-turbo', temperature=0.7):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message_history,
            temperature=temperature,
            max_tokens=1000,
        )
        assistant_reply = response['choices'][0]['message']['content']
        self.add_assistant_message(assistant_reply)

        return assistant_reply

    async def analyze_image(self, image_stream: BytesIO):
        """Отправляет изображение в GPT-4o для анализа"""

        image_base64 = base64.b64encode(image_stream.getvalue()).decode("utf-8")

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                #                {"role": "system", "content": 'Identify what is in the picture and describe it.'},
                {"role": "user", "content": [
                    {"type": "text", "text": "What is in this image?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]}
            ],
            max_tokens=500,
            temperature=0.5
        )

        return response['choices'][0]['message']['content']
