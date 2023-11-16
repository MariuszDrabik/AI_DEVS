import datetime
import uuid
import requests
from sqlalchemy import (
    TEXT,
    UUID,
    Column,
    Integer,
    String,
)
from db.database import POSTGRES_URL, Base, get_db, engine
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import (
    ChatInteraction,
    HumanMessage,
    Prompt,
    SystemMessage,
)


now = datetime.datetime.utcnow


class Person(Base):
    __tablename__ = "persons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    imie = Column(String)
    nazwisko = Column(TEXT)
    wiek = Column(Integer)
    o_mnie = Column(String)
    ulubiona_postac_z_kapitana_bomby = Column(String)
    ulubiony_serial = Column(String)
    ulubiony_film = Column(String)
    ulubiony_kolor = Column(String)

    def show(self):
        print(f"{self.imie}, {self.nazwisko}")


def get_people():
    header = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95"
            " Safari/537.36"
        )
    }
    response = requests.get(
        "https://zadania.aidevs.pl/data/people.json",
        headers=header,
        timeout=(200, 120),
    )
    return response.json()


def feed_base(persons):
    client = QdrantClient("localhost", port=6333)
    points = []
    for person in persons:
        print("*" * 50)
        print(person.id, person.imie)
        embedding = ChatInteraction().get_embedding(
            f"{person.imie} {person.nazwisko}"
        )
        print(embedding)
        points.append(
            PointStruct(
                id=str(person.id),
                vector=embedding,
            )
        )
        print("*" * 50)

    operation_info = client.upsert(
        collection_name="persons", wait=True, points=points
    )
    print(operation_info)


if __name__ == "__main__":
    print(POSTGRES_URL)
    client = QdrantClient("localhost", port=6333)

    task = "people"
    playground = AIDevPlayground(task)

    question = playground.get_task()["question"]
    print("QUESTION: ", question)
    embedding = ChatInteraction().get_embedding(f"{question}")

    search_result = client.search(
        collection_name="persons", query_vector=embedding, limit=3
    )
    person = None
    with get_db() as db:
        person = db.query(Person).filter_by(id=search_result[0].id).first()
        print("*" * 50)
        print(person.__dict__)
        print("*" * 50)

        if "kolor" in question:
            print(
                playground.check_answer(
                    {
                        "answer": (
                            f"Ulubiony kolor {person.imie},"
                            f" {person.nazwisko} {person.ulubiony_kolor}"
                        )
                    }
                )
            )
        elif "film" in question:
            print(
                playground.check_answer(
                    {
                        "answer": (
                            f"Ulubiony film {person.imie},"
                            f" {person.nazwisko} {person.ulubiony_film}"
                        )
                    }
                )
            )
        elif "serial" in question:
            print(
                playground.check_answer(
                    {
                        "answer": (
                            f"Ulubiony serial {person.imie},"
                            f" {person.nazwisko} {person.ulubiony_serial}"
                        )
                    }
                )
            )
        elif "wieku" in question:
            print(
                playground.check_answer(
                    {
                        "answer": (
                            f"{person.imie},"
                            f" {person.nazwisko} ma {person.wiek} lat"
                        )
                    }
                )
            )
        else:
            print(f"INFO:   {person.o_mnie}")
            msg_sys = SystemMessage(
                f"""Odpowiedz na pytanie. Be concise.
                    '''Context
                    imie: {person.imie}
                    Nazwisko: {person.nazwisko}
                    {person.o_mnie}
                                    """
            )
            msg_user = HumanMessage(f"Question {question}")
            prompt = Prompt([msg_sys, msg_user]).get_messages()
            answer = ChatInteraction(prompt).get_choices()
            print("ROBOT: ", answer)
            print(playground.check_answer({"answer": answer}))

    # print(all_people)
