from datetime import date
import json
import os
from dotenv import load_dotenv

import requests
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import (
    ChatInteraction,
    HumanMessage,
    Prompt,
    SystemMessage,
)

load_dotenv()


def get_data(url) -> dict[str, str]:
    response = requests.get(
        f"{url}",
        timeout=450,
    )
    return response.json()


if __name__ == "__main__":
    task = "optimaldb"
    playground = AIDevPlayground(task)
    question = playground.get_task()
    print(question)
    json = "https://zadania.aidevs.pl/data/3friends.json"
    json = get_data(json)
    print(type(json))

    files = ["person_zygfryd", "person_stefan", "person_ania"]
    base = ""
    for file in files:
        with open(f"{file}", "r", encoding="utf-8") as file_handler:
            data = file_handler.readlines()[0]
            base += f"{data} \n\n"

    print(base)

    print(playground.check_answer({"answer": base}))

    # for person, data in json.items():
    #     system = SystemMessage(
    #         """ Compress data. Remove duplicated info.
    #         """
    #     )

    #     user = HumanMessage(f"data to process: {data}")
    #     print(person, data)
    #     print("*" * 50)
    #     print("*" * 50)
    #     print("*" * 50)
    #     chat = ChatInteraction(Prompt([system, user]).get_messages())
    #     database = chat.get_choices()
    #     print("-" * 50)
    #     print(database)
    #     print("-" * 50)
    #     with open(f"person_{person}", "a", encoding="utf-8") as file_handler:
    #         file_handler.write(database)
