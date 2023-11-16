import json
import requests
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import (
    ChatInteraction,
    HumanMessage,
    Prompt,
    SystemMessage,
)


def get_population(country):
    header = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95"
            " Safari/537.36"
        )
    }
    response = requests.get(
        f"https://restcountries.com/v3.1/name/{country}?fields=population",
        headers=header,
        timeout=(200, 120),
    )
    return response.json()[0]["population"]


def get_exchange_rate(currency_code):
    header = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95"
            " Safari/537.36"
        ),
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"https://api.nbp.pl/api/exchangerates/rates/A/{currency_code}/?format=json",
        headers=header,
        timeout=(200, 120),
    )
    return response.json()["rates"][0]["mid"]


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_population",
            "description": "Get current population on giving location",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": (
                            "Country to check population e.g. Germany"
                        ),
                    },
                },
                "required": ["country"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get exchange rate to give currency",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency_code": {
                        "type": "string",
                        "description": (
                            "currency code to check e.g. EUR or HUF"
                        ),
                    },
                },
                "required": ["currency"],
            },
        },
    },
]


if __name__ == "__main__":
    task = "knowledge"
    playground = AIDevPlayground(task)
    question = playground.get_task()

    print(question)

    system = SystemMessage(
        """
            You have to answer on question. You got tools for that,
            if question do not match any tool try answer base on Your knowledge
            in Polish
        """
    )
    user = HumanMessage(f"{question}")

    chat = ChatInteraction(Prompt([system, user]).get_messages())

    message, tool_calls = chat.get_function(tools)
    if tool_calls:
        available_functions = {
            "get_population": get_population,
            "get_exchange_rate": get_exchange_rate,
        }
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)

            print(playground.check_answer({"answer": function_response}))
            print("FUNCTION: ", function_response)
    else:
        print("MESSAGE: ", message.get("content"))
        print(playground.check_answer({"answer": message.get("content")}))
