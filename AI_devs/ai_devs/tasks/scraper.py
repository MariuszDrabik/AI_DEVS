import json
import logging
import requests
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction, Message, Prompt


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_text(endpoint) -> None:
    header = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95"
            " Safari/537.36"
        )
    }
    response = requests.get(
        f"{endpoint}",
        headers=header,
        timeout=(200, 120),
    )
    return response


def main():
    code = 400
    text = ""
    task = "scraper"

    playground = AIDevPlayground(task)
    task = playground.get_task()
    log.info(task["input"])

    for _ in range(0, 10):
        try:
            response = get_text(task["input"])
            code = response.status_code
            if code == 200:
                text = response.text
                break
        except requests.exceptions.Timeout as error:
            print("Request has timed out", error)

    if code == 200:
        msg_system = Message(
            "system",
            f"""{task['msg']},

                ```CONTEXT
                {text}
            """,
        )

        msg_user = Message(
            "user",
            f"""{task['question']},
            """,
        )
        print(
            "aaaaa",
            Prompt(
                [msg_system.get_message, msg_user.get_message]
            ).get_messages(),
        )
        asystent = ChatInteraction(
            Prompt(
                [msg_system.get_message, msg_user.get_message]
            ).get_messages()
        )

        completion = asystent.get_choices()

        task_answer = playground.check_answer({"answer": f"{completion}"})

        log.info(task_answer)


if __name__ == "__main__":
    main()
