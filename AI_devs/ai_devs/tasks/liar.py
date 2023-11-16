import logging
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction, Message, Prompt


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if __name__ == "__main__":
    task = "liar"

    playground = AIDevPlayground(task)

    question = "Co jest stolicą Polski?"
    answer = playground.get_answer_from_bot({"question": question})

    log.info(answer)

    msg1 = Message(
        role="system",
        content=(
            f"""
            You are a answer validator. We have answer for question form BOT.
            You should check that answer from BOT if is proper or not.

                question:{question}

            """
            + """
                As BOT validator You should answer YES / NO in JSON FORMAT:
                {"answer": "YES"} If answer for question is proper
                {"answer": "NO"} If answer for question is not valid
            """
        ),
    )
    msg2 = Message(role="user", content=f"Bot answer: {answer}")

    guard = ChatInteraction(
        Prompt([msg1.get_message, msg2.get_message]).get_messages()
    )

    completion = guard.get_choices()
    log.info(completion)

    check = playground.check_answer(completion)
    log.info(check)
