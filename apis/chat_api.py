import argparse
import markdown2
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
from conversations import (
    ConversationConnector,
    ConversationCreator,
    MessageComposer,
)
from utils.logger import logger


class ChatAPIApp:
    def __init__(self):
        self.app = FastAPI(
            docs_url="/",
            title="Bing Chat API",
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            version="1.0",
        )
        self.setup_routes()
        self.app.mount("/docs", StaticFiles(directory="docs", html=True), name="docs")

    def get_available_models(self):
        self.available_models = {
            "object": "list",
            "data": [
                {
                    "id": "precise",
                    "description": "Bing (Precise): Concise and straightforward.",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "bing",
                },
                {
                    "id": "balanced",
                    "description": "Bing (Balanced): Informative and friendly.",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "bing",
                },
                {
                    "id": "creative",
                    "description": "Bing (Creative): Original and imaginative.",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "bing",
                },
                {
                    "id": "precise-offline",
                    "description": "Bing (Precise): (No Internet) Concise and straightforward.",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "bing",
                },
                {
                    "id": "balanced-offline",
                    "description": "Bing (Balanced): (No Internet) Informative and friendly.",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "bing",
                },
                {
                    "id": "creative-offline",
                    "description": "Bing (Creative): (No Internet) Original and imaginative.",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "bing",
                },
            ],
        }
        return self.available_models

    class CreateConversationSessionPostItem(BaseModel):
        model: str = Field(
            default="precise",
            description="(str) `precise`, `balanced`, `creative`, `precise-offline`, `balanced-offline`, `creative-offline`",
        )

    def create_conversation_session(self, item: CreateConversationSessionPostItem):
        creator = ConversationCreator()
        creator.create()
        return {
            "model": item.model,
            "sec_access_token": creator.sec_access_token,
            "client_id": creator.client_id,
            "conversation_id": creator.conversation_id,
        }

    class ChatCompletionsPostItem(BaseModel):
        model: str = Field(
            default="precise",
            description="(str) `precise`, `balanced`, `creative`, `precise-offline`, `balanced-offline`, `creative-offline`",
        )
        messages: list = Field(
            default=[{"role": "user", "content": "Hello, who are you?"}],
            description="(list) Messages",
        )

    def chat_completions(self, item: ChatCompletionsPostItem):
        creator = ConversationCreator()
        creator.create()

        connector = ConversationConnector(
            conversation_style=item.model,
            sec_access_token=creator.sec_access_token,
            client_id=creator.client_id,
            conversation_id=creator.conversation_id,
            cookies=creator.request_cookies,
            invocation_id=0,
        )

        message_composer = MessageComposer()
        prompt = message_composer.merge(item.messages)
        logger.mesg(item.messages[-1]["content"])
        system_prompt = message_composer.system_prompt

        return EventSourceResponse(
            connector.stream_chat(
                prompt=prompt, system_prompt=system_prompt, yield_output=True
            ),
            ping=2000,
            media_type="text/event-stream",
        )

    def get_readme(self):
        readme_path = Path(__file__).parents[1] / "README.md"
        with open(readme_path, "r", encoding="utf-8") as rf:
            readme_str = rf.read()
        readme_html = markdown2.markdown(
            readme_str, extras=["table", "fenced-code-blocks", "highlightjs-lang"]
        )
        return readme_html

    def setup_routes(self):
        for prefix in ["", "/v1", "/api", "/api/v1"]:
            include_in_schema = True if prefix == "" else False
            self.app.get(
                prefix + "/models",
                summary="Get available models",
                include_in_schema=include_in_schema,
            )(self.get_available_models)

            self.app.post(
                prefix + "/create",
                summary="Create a conversation session",
                include_in_schema=include_in_schema,
            )(self.create_conversation_session)

            self.app.post(
                prefix + "/chat/completions",
                summary="Chat completions in conversation session",
                include_in_schema=include_in_schema,
            )(self.chat_completions)

        self.app.get(
            "/readme",
            summary="README of Bing Chat API",
            response_class=HTMLResponse,
            include_in_schema=False,
        )(self.get_readme)


class ArgParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgParser, self).__init__(*args, **kwargs)

        self.add_argument(
            "-s",
            "--server",
            type=str,
            default="0.0.0.0",
            help="Server IP for Bing Chat API",
        )
        self.add_argument(
            "-p",
            "--port",
            type=int,
            default=22222,
            help="Server Port for Bing Chat API",
        )

        self.add_argument(
            "-d",
            "--dev",
            default=False,
            action="store_true",
            help="Run in dev mode",
        )

        self.args = self.parse_args(sys.argv[1:])


app = ChatAPIApp().app

if __name__ == "__main__":
    args = ArgParser().args
    if args.dev:
        uvicorn.run("__main__:app", host=args.server, port=args.port, reload=True)
    else:
        uvicorn.run("__main__:app", host=args.server, port=args.port, reload=False)

    # python -m apis.chat_api      # [Docker] on product mode
    # python -m apis.chat_api -d   # [Dev]    on develop mode
