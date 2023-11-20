import aiohttp
import asyncio
import httpx
import json
import pprint
import urllib

from chathub_request_constructor import ChathubRequestConstructor


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
            "Sec-Websocket-Version": "13",
            "Upgrade": "websocket",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }
        wss = await self.aio_session.ws_connect(
            self.ws_url,
            headers=request_headers,
            proxy=http_proxy,
        )

        await self._init_handshake(wss)
        chathub_request_construtor = ChathubRequestConstructor(
            prompt=prompt,
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
                        # pprint.pprint(throttling)
                    if arguments.get("messages"):
                        for message in arguments.get("messages"):
                            message_type = message.get("messageType")
                            if message_type is None:
                                # Displayed message does not contain 'messageType'
                                message_html = message["adaptiveCards"][0]["body"][0][
                                    "text"
                                ]
                                delta_content = message_html[delta_content_pointer:]
                                print(delta_content, end="", flush=True)
                                delta_content_pointer = len(message_html)

                                if message.get("suggestedResponses"):
                                    print("\nSuggested Questions: ", flush=True)
                                    for suggestion in message.get("suggestedResponses"):
                                        suggestion_text = suggestion.get("text")
                                        print(f"- {suggestion_text}", flush=True)

                            elif message_type in ["InternalSearchQuery"]:
                                message_hidden_text = message["hiddenText"]
                                print(
                                    f"\n[Searching: [{message_hidden_text}]]",
                                    flush=True,
                                )
                            elif message_type in [
                                "InternalSearchResult",
                            ]:
                                print("[Analyzing search results ...]", flush=True)
                            elif message_type in ["InternalLoaderMessage"]:
                                print("[Generating answers ...]\n", flush=True)
                            elif message_type in ["RenderCardRequest"]:
                                continue
                            else:
                                raise NotImplementedError(
                                    f"Not Supported Message Type: {message_type}"
                                )

                elif data.get("type") == 2:
                    if data.get("item"):
                        item = data.get("item")
                        print("\n[Saving chat messages ...]")
                        # for message in item.get("messages"):
                        #     author = message["author"]
                        #     message_text = message["text"]
                elif data.get("type") == 3:
                    print("[Finished]")
                    await wss.close()
                    break
                elif data.get("type") == 6:
                    continue
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
    prompt = "Today's weather of California"
    print(f"\n[User]: {prompt}\n")
    print(f"[Bing]:")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chatter.stream_chat(prompt=prompt))
    loop.close()
