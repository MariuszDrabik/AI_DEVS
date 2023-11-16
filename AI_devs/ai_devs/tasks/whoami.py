import json
import logging
import requests
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import (
    ChatInteraction,
    HumanMessage,
    Message,
    Prompt,
    SystemMessage,
)


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def main():
    task = "whoami"
    answer = ""
    check = "this is NOT the correct answer"
    hints = ""
    count = 0

    while check == "this is NOT the correct answer":
        playground = AIDevPlayground(task)

        whoami = playground.get_task()
        check = playground.check_answer(answer={"answer": f"{answer}"})["msg"]

        log.info(check)
        log.info(whoami["hint"])

        count += 1
        hints += f'hint {count}: {whoami["hint"]} \n '
        system = SystemMessage(
            "Guess person based on hints. If You don`t now. Simple answer no"
        )
        human = HumanMessage(hints)
        chat = ChatInteraction(Prompt([system, human]).get_messages())
        answer = chat.get_choices()
        log.info(answer)
        log.info("*" * 50)


if __name__ == "__main__":
    main()
