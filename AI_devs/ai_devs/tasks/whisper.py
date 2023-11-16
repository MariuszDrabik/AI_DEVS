import logging
import re
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction, Message, Prompt


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if __name__ == "__main__":
    task = "whisper"

    playground = AIDevPlayground(task)

    log.info(task)

    task = playground.get_task()

    log.info(task)
    url = re.search(
        r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .-]*", task["msg"]
    ).group()
    log.info(url)
    transcription = ChatInteraction().get_transcription(url)

    check_answer = playground.check_answer({"answer": transcription})

    log.info(check_answer)
