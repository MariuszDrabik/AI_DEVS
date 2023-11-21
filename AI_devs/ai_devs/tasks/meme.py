from datetime import date
import json
import os
from dotenv import load_dotenv

import requests
from utils.AIDevs import AIDevPlayground

load_dotenv()


def get_img(img, text) -> dict[str, str]:
    header = {
        "X-API-KEY": os.environ.get("RENDERFORM"),
        "Content-Type": "application/json",
    }
    body = {
        "template": "brawny-dragonflies-moan-easily-1503",
        "data": {
            "text.text": text,
            "image.src": img,
        },
    }
    response = requests.post(
        "https://api.renderform.io/api/v2/render",
        headers=header,
        json=body,
        timeout=450,
    )
    return response.json()


if __name__ == "__main__":
    task = "meme"
    playground = AIDevPlayground(task)
    question = playground.get_task()

    img = question["image"]
    text = question["text"]
    # render = get_img(img, text)
    render = "https://cdn.renderform.io/Xm4nitCJa1ZsidXbCaWU/results/req-cab6b682-1879-420c-9d9c-8e89099b566c.jpg"
    # breakpoint()
    print(render)
    print(playground.check_answer({"answer": render}).json())
