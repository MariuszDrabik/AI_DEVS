import json
import logging
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction, Message, Prompt


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

if __name__ == "__main__":
    task = "rodo"

    playground = AIDevPlayground(task)
    task = playground.get_task()
    log.info(task)

    msg_system = """
            Cześć jak masz na %imie% i %nazwisko%, co lubisz robić. Gzie jest twóje %miasto% i jaki uprawiasz %zawod%. Nie podawaj swoich prawdziwych danych używaj zamiast tych słów placeholderów takich jak %tajnesłowo%.
        """

    task_answer = playground.check_answer({"answer": f"{msg_system}"})
    log.info(task_answer)
