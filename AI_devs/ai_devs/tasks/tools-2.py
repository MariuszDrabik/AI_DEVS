from datetime import date
import json
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import (
    ChatInteraction,
    HumanMessage,
    Prompt,
    SystemMessage,
)


def tool_todo(desc, tool="ToDo"):
    return {"tool": tool, "desc": desc}


def tool_calendar(desc, date, tool="Calendar"):
    return {"tool": tool, "desc": desc, "date": date}


tools = [
    {
        "type": "function",
        "function": {
            "name": "ToDo",
            "description": "get to_do task",
            "parameters": {
                "type": "object",
                "properties": {
                    "desc": {
                        "type": "string",
                        "description": "Description of task",
                    },
                },
                "required": ["desc"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Calendar",
            "description": "put info/meeting to calender",
            "parameters": {
                "type": "object",
                "properties": {
                    "desc": {
                        "type": "string",
                        "description": "meeting description",
                    },
                    "date": {
                        "type": "string",
                        "description": "date in format YYYY-MM-DD",
                    },
                },
                "required": ["desc", "date"],
            },
        },
    },
]


if __name__ == "__main__":
    task = "tools"
    playground = AIDevPlayground(task)
    question = playground.get_task()

    print(question)

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
    user = HumanMessage(f"{question}")

    chat = ChatInteraction(Prompt([system, user]).get_messages())

    message = chat.get_choices()
    print(message)
    print(playground.check_answer({"answer": json.loads(message)}))
