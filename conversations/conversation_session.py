import asyncio
from conversations import ConversationCreator, ConversationConnector
from utils.logger import logger


class ConversationSession:
    def __init__(
        self,
        conversation_style: str = "precise",
        creator=None,
        connector=None,
    ):
        self.conversation_style = conversation_style
        self.creator = creator
        self.connector = connector

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def create(self):
        self.creator = ConversationCreator()
        self.creator.create()

    def connect(self):
        if self.connector is None:
            self.create()
            self.connector = ConversationConnector(
                conversation_style=self.conversation_style,
                sec_access_token=self.creator.sec_access_token,
                client_id=self.creator.client_id,
                conversation_id=self.creator.conversation_id,
                invocation_id=0,
            )

    def open(self):
        self.connect()
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

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
