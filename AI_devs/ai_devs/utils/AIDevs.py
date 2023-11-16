import os
from dotenv import load_dotenv
import requests

load_dotenv()


class AIDevPlayground:
    def __init__(self, task: str) -> None:
        self.api_key = os.environ.get("API")
        self.task = task
        self.endpoint = "https://zadania.aidevs.pl/"
        self.get_token()

    def get_token(self) -> None:
        response = requests.post(
            f"{self.endpoint}token/{self.task}",
            json={"apikey": self.api_key},
            timeout=450,
        )
        self.token = response.json()["token"]

    def get_task(self) -> dict:
        response = requests.get(
            f"{self.endpoint}/task/{self.token}",
            json={"apikey": self.api_key},
            timeout=450,
        )
        return response.json()

    def check_answer(self, answer: dict["str", "str"]) -> dict:
        response = requests.post(
            f"{self.endpoint}/answer/{self.token}",
            json=answer,
            timeout=450,
        )
        return response.json()

    def get_answer_from_bot(self, answer: dict[str, tuple]) -> dict:
        response = requests.post(
            f"{self.endpoint}/task/{self.token}",
            data=answer,
            timeout=450,
        )
        return response.json()
