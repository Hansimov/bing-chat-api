import httpx
import json
import pprint

http_proxy = "http://localhost:11111"  # Replace with yours


class ConversationCreator:
    conversation_create_url = "https://www.bing.com/turing/conversation/create"

    def __init__(self, cookies={}):
        self.cookies = cookies
        self.construct_cookies()

    def construct_cookies(self):
        self.httpx_cookies = httpx.Cookies()
        for key, val in self.cookies.items():
            self.httpx_cookies.set(key, val)

    def create(self, proxy=None):
        self.response = httpx.get(
            self.conversation_create_url,
            proxies=http_proxy if proxy is None else proxy,
            cookies=self.httpx_cookies,
        )
        self.response_content = json.loads(self.response.content.decode("utf-8"))
        self.response_headers = dict(self.response.headers)
        pprint.pprint(self.response_content)
        # pprint.pprint(self.response_headers)


if __name__ == "__main__":
    creator = ConversationCreator()
    creator.create()
