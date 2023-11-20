import random
import uuid


class ChathubRequestConstructor:
    def __init__(
        self,
        prompt,
        client_id: str,
        conversation_id: str,
        invocation_id: int = 0,
        conversation_style: str = "precise",
    ):
        self.prompt = prompt
        self.client_id = client_id
        self.conversation_id = conversation_id
        self.invocation_id = invocation_id
        self.conversation_style = conversation_style
        self.message_id = self._generate_random_uuid()
        self.construct()

    def _generate_random_uuid(self):
        return str(uuid.uuid4())

    def _generate_random_hex_str(self, length: int = 32) -> str:
        return "".join(random.choice("0123456789abcdef") for _ in range(length))

    def construct(self):
        self.request_message = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": [
                        "nlu_direct_response_filter",
                        "deepleo",
                        "disable_emoji_spoken_text",
                        "responsible_ai_policy_235",
                        "enablemm",
                        "dv3sugg",
                        "autosave",
                        "uquopt",
                        "enelecintl",
                        "gndeleccf",
                        "gndlogcf",
                        "logprobsc",
                        "fluxprod",
                        "eredirecturl",
                    ],
                    "allowedMessageTypes": [
                        "ActionRequest",
                        "Chat",
                        "ConfirmationCard",
                        "Context",
                        "InternalSearchQuery",
                        "InternalSearchResult",
                        "Disengaged",
                        "InternalLoaderMessage",
                        "InvokeAction",
                        "Progress",
                        "RenderCardRequest",
                        "RenderContentRequest",
                        "AdsQuery",
                        "SemanticSerp",
                        "GenerateContentQuery",
                        "SearchQuery",
                    ],
                    "sliceIds": [
                        "cruisecf",
                        "adssqovr",
                        "gbacf",
                        "bggrey",
                        "1366cf",
                        "vnextvoice",
                        "caccnctat3",
                        "specedgecf",
                        "inosanewsmob",
                        "wrapnoins",
                        "readaloud",
                        "autotts",
                        "styleoffall",
                        "rwt2",
                        "dismmaslp",
                        "1117gndelecs0",
                        "713logprobsc",
                        "1118wcpdcl",
                        "1119backos",
                        "1103gndlog",
                        "1107reviewss0",
                        "fluxnosearch",
                        "727nrprdrt3",
                        "codecreator1",
                        "kchero50cf",
                        "cacmuidarb",
                    ],
                    "verbosity": "verbose",
                    "scenario": "SERP",
                    "plugins": [
                        {"id": "c310c353-b9f0-4d76-ab0d-1dd5e979cf68"},
                    ],
                    "traceId": self._generate_random_hex_str(),
                    "conversationHistoryOptionsSets": [
                        "autosave",
                        "savemem",
                        "uprofupd",
                        "uprofgen",
                    ],
                    "isStartOfSession": self.invocation_id == 0,
                    "requestId": self.message_id,
                    "message": {
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": self.prompt,
                        "messageType": "Chat",
                        "requestId": self.message_id,  # "a6ecd3aa-1007-6959-52fb-9e23f34e86be",
                        "messageId": self.message_id,  # "a6ecd3aa-1007-6959-52fb-9e23f34e86be",
                    },
                    "tone": self.conversation_style.capitalize(),
                    "spokenTextMode": "None",
                    "conversationId": self.conversation_id,  # "51D|BingProdUnAuthenticatedUsers|65761F31183134340AFD8F9AF1532EA90DC7F11ED348765DE9BAC956C9BA4669",
                    "participant": {
                        "id": self.client_id,  # "23EBCCB7073868D70172DF780674692D",
                    },
                }
            ],
            "invocationId": str(self.invocation_id),
            "target": "chat",
            "type": 4,
        }
