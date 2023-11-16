from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import requests
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import ChatInteraction
import uuid

client = QdrantClient("localhost", port=6333)

task = "search"
playground = AIDevPlayground(task)

print(playground.get_task())

embedding = ChatInteraction().get_embedding(playground.get_task()["question"])

search_result = client.search(
    collection_name="unknow.news",
    query_vector=embedding,
    limit=1,
)
print(playground.check_answer({"answer": search_result[0].payload["url"]}))

print(search_result)


def get_news():
    header = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95"
            " Safari/537.36"
        )
    }
    response = requests.get(
        f"https://unknow.news/archiwum.json",
        headers=header,
        timeout=(200, 120),
    )
    return response.json()


def feed_base():
    points = []
    for news in get_news()[0:300]:
        print("*" * 50)
        print(news["info"].replace("INFO: ", ""))
        embedding = ChatInteraction().get_embedding(
            news["info"].replace("INFO: ", "")
        )
        print(embedding)
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "url": news["url"],
                    "title": news["title"],
                    "date": news["date"],
                },
            )
        )
        print("*" * 50)
    operation_info = client.upsert(
        collection_name="unknow.news", wait=True, points=points
    )
    print(operation_info)

    test = uuid.uuid4()
    print(str(test))
