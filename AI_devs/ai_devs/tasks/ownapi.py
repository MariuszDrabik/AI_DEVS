from datetime import date
import json
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import (
    ChatInteraction,
    HumanMessage,
    Prompt,
    SystemMessage,
)

if __name__ == "__main__":
    task = "ownapipro"
    playground = AIDevPlayground(task)
    question = playground.get_task()
    print(question)
    url = "https://ai_devs.nextwww.pl/ai_pro"
    # playground.check_answer({"answer": url})
    print(playground.check_answer({"answer": url}))
