import json
import logging
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction, Message, Prompt


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# answer1 = {
#     "answer": {
#         "name": "addUser",
#         "description": "add new user",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "name": {
#                     "type": "string",
#                     "description": "user`s name",
#                 },
#                 "surname": {
#                     "type": "string",
#                     "description": "user`s surname",
#                 },
#                 "year": {
#                     "type": "integer",
#                     "description": "user`s birth year",
#                 },
#             },
#         },
#     }
# }
hint3 = {
    "answer": {
        "name": "orderPizza",
        "description": "select pizza in pizzeria based on pizza name",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "provide name of the pizza",
                }
            },
        },
    }
}


if __name__ == "__main__":
    task = "functions"

    playground = AIDevPlayground(task)
    task = playground.get_task()
    log.info(task)

    msg_system = Message("system", f"{task['msg']}")
    msg_user = Message(
        "user",
        f"""Two hints: 1:{task['hint1']} 2:{task['hint1']}
            IMPORTANT!!!! You must send me back only JSON format LIKE: {hint3}.
            use double quoted
        """,
    )
    prompt = Prompt([msg_system.get_message, msg_user.get_message])
    messages = prompt.get_messages()

    log.info(messages)

    send_to_chat = ChatInteraction(messages)
    chat_answer = send_to_chat.get_choices()
    print(type(json.loads(chat_answer)))

    task_answer = playground.check_answer(json.loads(chat_answer))

    log.info(task_answer)
