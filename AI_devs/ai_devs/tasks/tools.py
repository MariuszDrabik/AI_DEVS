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

           example for ToDo: Przypomnij mi, że mam kupić mleko
           example for Calendar: Jutro mam spotkanie z Marianem

           ```CONTEXT
              today date is: {date.today()}
        """
    )
    user = HumanMessage(f"{question}")

    chat = ChatInteraction(Prompt([system, user]).get_messages())

    message, tool_calls = chat.get_function(tools)
    print(message, tool_calls)
    if tool_calls:
        available_functions = {
            "Calendar": tool_calendar,
            "ToDo": tool_todo,
        }
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            print(function_to_call)
            if function_args := json.loads(tool_call.function.arguments):
                function_response = function_to_call(**function_args)

            print(playground.check_answer({"answer": function_response}))
            print("FUNCTION: ", function_response)
