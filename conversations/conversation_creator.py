import httpx
import json
from pprint import pprint
from utils.enver import enver


class ConversationCreator:
    conversation_create_url = "https://www.bing.com/turing/conversation/create"

    def __init__(self, cookies: dict = {}):
        self.cookies = cookies

    def construct_cookies(self):
        self.httpx_cookies = httpx.Cookies()
        for key, val in self.cookies.items():
            self.httpx_cookies.set(key, val)

    def construct_headers(self):
        # New Bing 封锁原理探讨 #78
        # https://github.com/weaigc/bingo/issues/78
        self.request_headers = {
            "X-Forwarded-For": "65.49.22.66",
        }

    def create(self):
        self.construct_cookies()
        self.construct_headers()
        enver.set_envs(proxies=True)
        self.response = httpx.get(
            self.conversation_create_url,
            headers=self.request_headers,
            proxies=enver.envs.get("http_proxy") or None,
            cookies=self.httpx_cookies,
        )
        self.response_content = json.loads(self.response.content.decode("utf-8"))
        self.response_headers = dict(self.response.headers)
        pprint(self.response_content)

        # These info would be used in ConversationConnector
        self.sec_access_token = self.response_headers[
            "x-sydney-encryptedconversationsignature"
        ]
        self.client_id = self.response_content["clientId"]
        self.conversation_id = self.response_content["conversationId"]


if __name__ == "__main__":
    creator = ConversationCreator()
    creator.create()
