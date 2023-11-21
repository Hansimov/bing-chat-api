import uvicorn

from fastapi import FastAPI
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

    def setup_routes(self):
        self.app.get(
            "/models",
            summary="Get available models",
        )(self.get_available_models)


app = ChatAPIApp().app

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=22222, reload=True)
