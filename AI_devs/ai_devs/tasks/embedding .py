import logging
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction, Message, Prompt


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if __name__ == "__main__":
    task = "embedding"
    fraze = "Hawaiian pizza"

    playground = AIDevPlayground(task)

    task = playground.get_task()
    # text = task["input"]
    log.info(task)

    chat = ChatInteraction(Prompt([Message("", "")]))

    embedding = chat.get_embedding(fraze)
    log.info(embedding)

    is_good = playground.check_answer({"answer": embedding})

    log.info(is_good)
