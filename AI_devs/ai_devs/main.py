from datetime import date
import json
import logging
from typing import Dict
import uvicorn
from schemas.question import QuestionSchema, ReplySchama
from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from conf_dirs import ROOT_DIR
from config.log_conf import set_logger
from config.config import settings
from db.database import POSTGRES_URL
from utils.AIDevs import AIDevPlayground
from utils.OpenAiAPI import (
    ChatInteraction,
    HumanMessage,
    Prompt,
    SystemMessage,
)
from starlette_context import middleware, plugins, context

set_logger()

log = logging.getLogger("__name__")

app = FastAPI()

app.add_middleware(
    middleware.ContextMiddleware,
    plugins=(
        plugins.ForwardedForPlugin(),
    ),
)

app.mount(
    "/static",
    StaticFiles(directory=f"{ROOT_DIR}/static"),
    name="static",
)
router = APIRouter()


@app.get("/")
async def health_checker(request: Request, test: str = "", test_2: str = "" ) -> Dict[str, str]:
    forwarded_for = context.data["X-Forwarded-For"]
    print(forwarded_for)
    return {"message": f"Hello from FastAPI for AI DEVS {test_2 or ''} {test}"}

@app.post("/ai")
async def open_ai(question: QuestionSchema):
    return {"answer" : "do not do that"}

    {"answer" : "do not do that"}
    log.info(question.question)

    system = SystemMessage(
        f"""Anserw the question in string format only. Strickt as possible

        """
    )
    user = HumanMessage(f"{question.question}")
    chat = ChatInteraction(Prompt([system, user]).get_messages())
    message = chat.get_choices()

    print(message)
    print(type(message))


    log.info(f"health_checker {message}")

    return {"reply":message}

@app.post("/ai_pro")
async def open_ai(question: QuestionSchema):
    return {"answer" : "do not do that"}
    log.info(question.question)

    with open("convers.txt", "a") as file_handler:
        file_handler.write(question.question)

    context = open("convers.txt", "r")
    system = SystemMessage(
        f"""Anserw the questions in string format only. Strickt as possible.
            If user input is not a questionjust be kind and say hello or something like that

        ```CONTEXT
            {context.read()}
        """
    )
    context.close()
    user = HumanMessage(f"{question.question}")
    chat = ChatInteraction(Prompt([system, user]).get_messages())
    message = chat.get_choices()

    log.info(f"health_checker {message}")

    return {"reply":message}


@app.post("/ai_meme")
async def open_ai(question: QuestionSchema):
    return "Siema"
    system = SystemMessage(
        f"""Anserw the questions in string format only. Strickt as possible.
            If user input is not a questionjust be kind and say hello or something like that

        ```CONTEXT
            {context.read()}
        """
    )
    context.close()
    user = HumanMessage(f"{question.question}")
    chat = ChatInteraction(Prompt([system, user]).get_messages())
    message = chat.get_choices()

    log.info(f"health_checker {message}")

    return {"reply":message}


# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#         workers=1,
#         proxy_headers=True,
#         forwarded_allow_ips=""
#     )
