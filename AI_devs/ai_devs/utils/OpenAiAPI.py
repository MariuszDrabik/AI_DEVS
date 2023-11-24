from dataclasses import dataclass, field
import io
import os
import json
from dotenv import load_dotenv
import openai
from openai import OpenAI
import requests

load_dotenv()


@dataclass
class Message:
    role: str
    content: str

    @property
    def get_message(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
        }


@dataclass
class PromptMessage:
    content: str
    role: str

    @property
    def message(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
        }


@dataclass
class SystemMessage(PromptMessage):
    content: str
    role: str = "system"


@dataclass
class HumanMessage(PromptMessage):
    content: str
    role: str = "user"


@dataclass
class VisionMessage(PromptMessage):
    content: str
    role: str = "user"
    url: str = ""

    @property
    def message(self) -> dict:
        return {
            "role": f"{self.role}",
            "content": [
                {"type": "text", "text": f"{self.content}"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"{self.url}",
                    },
                },
            ],
        }


@dataclass
class Prompt:
    _messages: list[Message] = field(default_factory=list)

    def collect_messages(self, message: Message) -> None:
        self._messages.append(message.get_message())

    def get_messages(self):
        return [msg.message for msg in self._messages]


class ChatInteraction:
    client = OpenAI()

    def __init__(self, prompt: Prompt | None = None) -> None:
        self.openai = openai
        self.prompt = prompt
        # self.model: str = os.getenv("OPEN_MODEL")
        self.model: str = "gpt-4"
        self.api_key: str = os.getenv("OPENAI_API_KEY")
        self.openai.api_key: str = self.api_key

    def get_choices(self) -> dict:
        completion = self.openai.ChatCompletion.create(
            model=self.model, messages=self.prompt
        )
        message = completion.choices[0].message
        return message.content

    def get_choices_ft(self) -> dict:
        completion = self.openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal::8OXDIm0o",
            messages=self.prompt,
        )
        message = completion.choices[0].message
        return message.content

    def get_function(self, tools) -> tuple[str, str]:
        completion = self.openai.ChatCompletion.create(
            model=self.model, messages=self.prompt, tools=tools
        )
        message = completion.choices[0].message
        tool_calls = message.get("tool_calls")
        return message, tool_calls

    def get_vision(self) -> tuple[str, str]:
        completion = self.openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=self.prompt,
            max_tokens=300,
        )
        message = completion.choices[0]
        return message

    def get_embedding(self, message: str) -> list:
        response = requests.post(
            url="https://api.openai.com/v1/embeddings",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            json={
                "input": f"{[message]}",
                "model": "text-embedding-ada-002",
            },
            timeout=450,
        )
        message = response.json()["data"][0]["embedding"]
        return message

    def get_transcription(self, url):
        request = requests.get(url, allow_redirects=True, timeout=500)
        audio_handler = io.BytesIO()
        audio_handler.write(request.content)
        audio_handler.name = "mateusz.mp3"
        audio_handler.seek(0)  # cursor to file start

        file_to_send = io.BufferedReader(audio_handler)

        transcribe = openai.Audio.transcribe(
            model="whisper-1", file=file_to_send
        )
        return transcribe["text"]

    @classmethod
    def tuning_model_file(cls, file):
        cls.client.files.create(
            file=open(file, "rb"),
            purpose="fine-tune",
        )


if __name__ == "__main__":
    sm = SystemMessage("lalalalaalla")
    hm = HumanMessage("lalalalaalla")

    print(sm, hm)
