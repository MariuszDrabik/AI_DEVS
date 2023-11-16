import json
import logging
import os
import requests
from dotenv import load_dotenv
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction, Message, Prompt


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if __name__ == "__main__":
    # task = "helloapi"
    # task = "moderation"
    task = "blogger"

    playground = AIDevPlayground(task)
    playground.get_token()
    log.info(playground.get_task())

    task = playground.get_task()

    msg1 = Message(
        role="system",
        content="""please write blog post for the provided outline max 1 sentence for each in polish:
                            Wstęp: kilka słów na temat historii pizzy (użyj historia i napisz o królowej Marghericie),
                            Niezbędne składniki na pizzę, (wymiń składniki po przecinki)
                            Robienie pizzy, (podaj kroki)
                            Pieczenie pizzy w piekarniku

                            return blog post in JSON format:
                            {"answer":["tekst 1","tekst 2","tekst 3","tekst 4"]}"}""",
    )
    msg2 = Message(role="user", content="")

    prompt = Prompt([msg1.get_message, msg2.get_message]).get_messages()

    chat = ChatInteraction(prompt=prompt)

    answer = chat.get_choices()
    print("*" * 50)
    print(type(answer))
    print(type(json.loads(answer)))
    print("*" * 50)

    print(playground.check_answer(answer=json.loads(answer)))
