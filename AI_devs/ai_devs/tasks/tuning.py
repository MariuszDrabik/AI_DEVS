from datetime import date
from utils.OpenAiAPI import (
    ChatInteraction,
    HumanMessage,
    Prompt,
    SystemMessage,
)


if __name__ == "__main__":
    system = SystemMessage(
        f"""Decide whether the task should be added to the ToDo list or
           to the Calendar (if time is provided)
           always use YYYY-MM-DD format for dates
           return in JON FORMAT

           example for ToDo: Przypomnij mi, że mam kupić mleko = {{"tool":"ToDo","desc":"Kup mleko"}}
           example for Calendar: Jutro mam spotkanie z Marianem = {{"tool":"Calendar","desc":"Spotkanie z Marianem","date":"2023-11-16"}}

           ```CONTEXT
              today date is: {date.today()}
        """
    )
    user = HumanMessage("Ups")

    chat = ChatInteraction.tuning_model_file("data.jsonl")
