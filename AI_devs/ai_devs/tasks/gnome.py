from datetime import date
import json
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import (
    ChatInteraction,
    Prompt,
    VisionMessage,
)


if __name__ == "__main__":
    # task = "gnome"
    # playground = AIDevPlayground(task)
    # question = playground.get_task()

    # print(question)

    vision = VisionMessage(
        content="Diskarabe what is on picture",
        url="https://sfd-atelier.fr/wp-content/uploads/2020/10/fjaril-black-table-extensible-ronde-en-chene_sfd_furniture_design5.webp",
    )

    chat = ChatInteraction(Prompt([vision]).get_messages())

    message = chat.get_vision()
    print(message["message"]["content"])
    # print(playground.check_answer({"answer": message["message"]["content"]}))
