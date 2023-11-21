import asyncio
from conversation_creator import ConversationCreator
from conversation_connector import ConversationConnector
from logger.logger import logger


class ConversationSession:
    def __init__(self) -> None:
        pass

    def run(self):
        self.create()
        self.connect()

    def create(self):
        self.creator = ConversationCreator()
        self.creator.create()

    def connect(self):
        self.connector = ConversationConnector(
            sec_access_token=self.creator.response_headers[
                "x-sydney-encryptedconversationsignature"
            ],
            client_id=self.creator.response_content["clientId"],
            conversation_id=self.creator.response_content["conversationId"],
        )

    def open(self):
        self.event_loop = asyncio.get_event_loop()

    def close(self):
        self.event_loop.close()

    def chat(self, prompt):
        logger.success(f"\n[User]: ", end="")
        logger.mesg(f"{prompt}")
        logger.success(f"[Bing]:")
        self.event_loop.run_until_complete(self.connector.stream_chat(prompt=prompt))


if __name__ == "__main__":
    session = ConversationSession()
    session.run()
    session.open()
    prompts = [
        "Today's weather of California",
        "Please summarize your previous answer in table format",
    ]
    for prompt in prompts:
        session.chat(prompt)
    session.close()
