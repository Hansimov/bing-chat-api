import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
from conversations import (
    ConversationConnector,
    ConversationCreator,
    ConversationSession,
)


class ChatAPIApp:
    def __init__(self):
        self.app = FastAPI(
            docs_url="/",
            title="Bing Chat API",
            version="1.0",
        )
        self.setup_routes()

    def get_available_models(self):
        self.available_models = [
            {
                "id": "precise",
                "description": "Bing (Precise): Concise and straightforward.",
            },
            {
                "id": "balanced",
                "description": "Bing (Balanced): Informative and friendly.",
            },
            {
                "id": "creative",
                "description": "Bing (Creative): Original and imaginative.",
            },
            {
                "id": "precise-offline",
                "description": "Bing (Precise): (No Internet) Concise and straightforward.",
            },
            {
                "id": "balanced-offline",
                "description": "Bing (Balanced): (No Internet) Informative and friendly.",
            },
            {
                "id": "creative-offline",
                "description": "Bing (Creative): (No Internet) Original and imaginative.",
            },
        ]
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

    class ChatPostItem(BaseModel):
        prompt: str = Field(
            default="Hello, who are you?",
            description="(str) Prompt",
        )
        model: str = Field(
            default="precise",
            description="(str) `precise`, `balanced`, `creative`, `precise-offline`, `balanced-offline`, `creative-offline`",
        )
        sec_access_token: str = Field(
            default="",
            description="(str) Sec Access Token",
        )
        client_id: str = Field(
            default="",
            description="(str) Client ID",
        )
        conversation_id: str = Field(
            default="",
            description="(str) Conversation ID",
        )
        invocation_id: int = Field(
            default=0,
            description="(int) Invocation ID",
        )

    def chat(self, item: ChatPostItem):
        connector = ConversationConnector(
            conversation_style=item.model,
            sec_access_token=item.sec_access_token,
            client_id=item.client_id,
            conversation_id=item.conversation_id,
            invocation_id=item.invocation_id,
        )

        return EventSourceResponse(
            connector.stream_chat(prompt=item.prompt, yield_output=True),
            media_type="text/event-stream",
        )

    class ChatCompletionsPostItem(BaseModel):
        model: str = Field(
            default="precise",
            description="(str) `precise`, `balanced`, `creative`, `precise-offline`, `balanced-offline`, `creative-offline`",
        )
        messages: list = Field(
            default=[{"role": "user", "content": "Hello, who are you?"}],
            description="(list) Messages",
        )
        sec_access_token: str = Field(
            default="",
            description="(str) Sec Access Token",
        )
        client_id: str = Field(
            default="",
            description="(str) Client ID",
        )
        conversation_id: str = Field(
            default="",
            description="(str) Conversation ID",
        )
        invocation_id: int = Field(
            default=0,
            description="(int) Invocation ID",
        )

    def chat_completions(self, item: ChatCompletionsPostItem):
        connector = ConversationConnector(
            conversation_style=item.model,
            sec_access_token=item.sec_access_token,
            client_id=item.client_id,
            conversation_id=item.conversation_id,
            invocation_id=item.invocation_id,
        )

        if item.invocation_id == 0:
            # TODO: History Messages Merger
            prompt = item.messages[-1]["content"]
        else:
            prompt = item.messages[-1]["content"]

        return EventSourceResponse(
            connector.stream_chat(prompt=prompt, yield_output=True),
            media_type="text/event-stream",
        )

    def setup_routes(self):
        self.app.get(
            "/models",
            summary="Get available models",
        )(self.get_available_models)

        self.app.post(
            "/create",
            summary="Create a conversation session",
        )(self.create_conversation_session)

        self.app.post(
            "/chat",
            summary="Chat in conversation session",
        )(self.chat)

        self.app.post(
            "/chat/completions",
            summary="Chat completions in conversation session",
        )(self.chat_completions)


app = ChatAPIApp().app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=22222, reload=True)
