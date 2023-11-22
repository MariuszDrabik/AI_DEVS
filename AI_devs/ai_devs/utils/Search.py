

import requests


def get_embedding(self, message: str) -> list:
    response = requests.post(
        url="https://serpapi.com/search",
        json={
            "engine": "google",
            "api-key":
        },
        timeout=450,
    )
    message = response.json()["data"][0]["embedding"]
    return message