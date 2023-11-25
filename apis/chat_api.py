import uvicorn

from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field
from conversations import ConversationSession


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
                "id": "bing-precise",
                "description": "Bing (Precise): Concise and straightforward.",
            },
            {
                "id": "bing-balanced",
                "description": "Bing (Balanced): Informative and friendly.",
            },
            {
                "id": "bing-creative",
                "description": "Bing (Creative): Original and imaginative.",
            },
            {
                "id": "bing-precise-offline",
                "description": "Bing (Precise): (No Internet) Concise and straightforward.",
            },
            {
                "id": "bing-balanced-offline",
                "description": "Bing (Balanced): (No Internet) Informative and friendly.",
            },
            {
                "id": "bing-creative-offline",
                "description": "Bing (Creative): (No Internet) Original and imaginative.",
            },
        ]
        return self.available_models

    async def create_conversation_session(
        self, websocket: WebSocket, conversation_style="precise"
    ):
        await websocket.accept()
        conversation_session = ConversationSession(conversation_style)
        conversation_session.open()
        while True:
            try:
                data = await websocket.receive_text()
                response = await conversation_session.chat(data)
                await websocket.send_text(response)
            except Exception as e:
                print(e)
                break

    def setup_routes(self):
        self.router = APIRouter()
        self.router.add_api_route("/models", self.get_available_models)
        self.router.add_websocket_route("/create", self.create_conversation_session)
        self.app.include_router(self.router)


app = ChatAPIApp().app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=22222, reload=True)
