import logging
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction, Message, Prompt


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if __name__ == "__main__":
    task = "inprompt"

    playground = AIDevPlayground(task)

    task = playground.get_task()
    text = task["input"]
    question = task["question"]
    msg = task["msg"]
    log.info(question)
    name = question.replace("?", "").split(" ")[-1]
    new_text = [sentence for sentence in text if name in sentence]
    log.info(name)
    log.info(new_text)
    msg1 = Message(
        role="system",
        content=f"""
                instruction: {msg}, answer as JSON "answer": "xyz"

                #####
                context: {new_text}
                #####
            """,
    )
    msg2 = Message(role="user", content=f"Question: {question}")

    asystent = ChatInteraction(Prompt([msg1.get_message, msg2.get_message]))

    completion = asystent.get_choices()
    log.info(completion)

    check = playground.check_answer(completion)
    log.info(check)
