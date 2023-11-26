import uvicorn

from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field
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
            "conversation_id": creator.conversation_id,
            "client_id": creator.client_id,
            "sec_access_token": creator.sec_access_token,
        }

    def setup_routes(self):
        self.app.get(
            "/models",
            summary="Get available models",
        )(self.get_available_models)

        self.app.post(
            "/create",
            summary="Create a conversation session",
        )(self.create_conversation_session)


app = ChatAPIApp().app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=22222, reload=True)
