import requests
from pprint import pprint
from utils.logger import logger
from utils.enver import enver
from networks import ConversationCreateHeadersConstructor
from networks import CookiesConstructor


class ConversationCreator:
    conversation_create_url = "https://www.bing.com/turing/conversation/create"

    def __init__(self, cookies: dict = {}):
        self.request_cookies = cookies

    def construct_cookies(self):
        cookies_constructor = CookiesConstructor()
        if not self.request_cookies:
            cookies_constructor.construct()
            self.request_cookies = cookies_constructor.cookies

    def construct_headers(self):
        # New Bing 封锁原理探讨 #78
        # https://github.com/weaigc/bingo/issues/78
        self.request_headers = ConversationCreateHeadersConstructor().request_headers

    def create(self):
        self.construct_cookies()
        self.construct_headers()
        enver.set_envs(proxies=True)
        self.response = requests.get(
            self.conversation_create_url,
            headers=self.request_headers,
            proxies=enver.requests_proxies,
            cookies=self.request_cookies,
        )
        try:
            self.response_data = self.response.json()
        except:
            print(self.response.text)
            raise Exception(
                f"x Failed to create conversation: {self.response.status_code}"
            )
        self.response_headers = self.response.headers
        pprint(self.response_data)

        # These info would be used in ConversationConnector
        self.sec_access_token = self.response_headers[
            "x-sydney-encryptedconversationsignature"
        ]
        self.client_id = self.response_data["clientId"]
        self.conversation_id = self.response_data["conversationId"]


if __name__ == "__main__":
    creator = ConversationCreator()
    creator.create()
