import asyncio
from conversation_creator import ConversationCreator
from conversation_connector import ConversationConnector
from logger.logger import logger


class ConversationSession:
    def __init__(self, conversation_style: str = "precise"):
        self.conversation_style = conversation_style

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def create(self):
        self.creator = ConversationCreator()
        self.creator.create()

    def connect(self):
        self.connector = ConversationConnector(
            conversation_style=self.conversation_style,
            sec_access_token=self.creator.sec_access_token,
            client_id=self.creator.client_id,
            conversation_id=self.creator.conversation_id,
        )

    def open(self):
        self.create()
        self.connect()
        self.event_loop = asyncio.get_event_loop()

    def close(self):
        self.event_loop.close()

    def chat(self, prompt):
        logger.success(f"\n[User]: ", end="")
        logger.mesg(f"{prompt}")
        logger.success(f"[Bing]:")
        self.event_loop.run_until_complete(self.connector.stream_chat(prompt=prompt))


if __name__ == "__main__":
    prompts = [
        "Today's weather of California",
        "Please summarize your previous answer in table format",
    ]
    with ConversationSession("precise") as session:
        for prompt in prompts:
            session.chat(prompt)
