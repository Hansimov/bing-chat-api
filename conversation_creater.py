import aiohttp
import asyncio
import certifi
import httpx
import json
import pprint
import ssl
import urllib

from chathub_request_constructor import ChathubRequestConstructor
from cookies_constructor import CookiesConstructor

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

http_proxy = "http://localhost:11111"


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


def serialize_websockets_message(msg: dict) -> str:
    return json.dumps(msg, ensure_ascii=False) + "\x1e"


class ConversationChatter:
    def __init__(
        self,
        sec_access_token=None,
        client_id=None,
        conversation_id=None,
        invocation_id=0,
        cookies={},
    ):
        self.sec_access_token = sec_access_token
        self.client_id = client_id
        self.conversation_id = conversation_id
        self.invocation_id = invocation_id
        self.cookies = cookies
        self.ws_url = (
            "wss://sydney.bing.com/sydney/ChatHub"
            + f"?sec_access_token={urllib.parse.quote(self.sec_access_token)}"
        )

    async def _init_handshake(self, wss):
        await wss.send_str(
            serialize_websockets_message({"protocol": "json", "version": 1})
        )
        await wss.receive_str()
        await wss.send_str(serialize_websockets_message({"type": 6}))

    async def stream_chat(self, prompt=""):
        self.aio_session = aiohttp.ClientSession(cookies=self.cookies)
        request_headers = {
            "Accept-Encoding": " gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "Upgrade",
            "Host": "sydney.bing.com",
            "Origin": "https://www.bing.com",
            "Pragma": "no-cache",
            "Sec-Websocket-Extensions": "permessage-deflate; client_max_window_bits",
            # "Sec-Websocket-Key": "**********************==",
            "Sec-Websocket-Version": "13",
            "Upgrade": "websocket",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }
        wss = await self.aio_session.ws_connect(
            self.ws_url,
            headers=request_headers,
            ssl=ssl_context,
            proxy=http_proxy,
        )

        await self._init_handshake(wss)
        chathub_request_construtor = ChathubRequestConstructor(
            prompt="Hello, tell me your name. No more than 3 words.",
            conversation_style="precise",
            client_id=self.client_id,
            conversation_id=self.conversation_id,
            invocation_id=self.invocation_id,
        )
        chathub_request_construtor.construct()

        await wss.send_str(
            serialize_websockets_message(chathub_request_construtor.request_message)
        )

        delta_content_pointer = 0
        while not wss.closed:
            response_lines_str = await wss.receive_str()
            if isinstance(response_lines_str, str):
                response_lines = response_lines_str.split("\x1e")
            else:
                continue
            for line in response_lines:
                if not line:
                    continue
                data = json.loads(line)
                if data.get("type") == 1:
                    arguments = data["arguments"][0]
                    if arguments.get("throttling"):
                        throttling = arguments.get("throttling")
                        pprint.pprint(throttling)
                    if arguments.get("messages"):
                        for message in arguments.get("messages"):
                            # html_str = messages["adaptiveCards"][0]["body"][0]["text"]
                            message_text = message["text"]
                            print(
                                message_text[delta_content_pointer:], end="", flush=True
                            )
                            delta_content_pointer = len(message_text)

                elif data.get("type") == 2:
                    if data.get("item"):
                        item = data.get("item")
                        for message in item.get("messages"):
                            author = message["author"]
                            message_text = message["text"]
                            # print(f"[{author}]: {message_text}")
                elif data.get("type") == 3:
                    print("[Finished]")
                    await wss.close()
                    break
                else:
                    # pprint.pprint(data)
                    continue


if __name__ == "__main__":
    creator = ConversationCreator()
    creator.create()

    chatter = ConversationChatter(
        sec_access_token=creator.response_headers[
            "x-sydney-encryptedconversationsignature"
        ],
        client_id=creator.response_content["clientId"],
        conversation_id=creator.response_content["conversationId"],
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chatter.stream_chat())
    loop.close()
