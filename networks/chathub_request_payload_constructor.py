import random
import uuid
from conversations import ConversationStyle


class SystemPromptContextConstructor:
    # https://github.com/weaigc/bingo/blob/eaebba306d5f68b940e4486ad81897516d0db0f3/src/lib/bots/bing/index.ts#L205-L211
    # https://github.com/weaigc/bingo/blob/eaebba306d5f68b940e4486ad81897516d0db0f3/src/lib/bots/bing/index.ts#L296
    def __init__(self, system_prompt: str = None):
        self.system_prompt = system_prompt
        self.construct()

    def construct(self):
        if self.system_prompt:
            self.system_context = [
                {
                    "author": "user",
                    "description": self.system_prompt,
                    "contextType": "WebPage",
                    "messageType": "Context",
                    "messageId": "discover-web--page-ping-mriduna-----",
                }
            ]
        else:
            self.system_context = None


class ChathubRequestPayloadConstructor:
    def __init__(
        self,
        prompt: str,
        client_id: str,
        conversation_id: str,
        invocation_id: int = 0,
        conversation_style: str = ConversationStyle.PRECISE.value,
        system_prompt: str = None,
    ):
        self.prompt = prompt
        self.client_id = client_id
        self.conversation_id = conversation_id
        self.invocation_id = invocation_id
        self.conversation_style = conversation_style.lower()

        if self.conversation_style.endswith("offline"):
            self.enable_search = False
            self.conversation_style = self.conversation_style.replace("-offline", "")
        else:
            self.enable_search = True

        self.message_id = self.generate_random_uuid()
        self.system_prompt = system_prompt
        self.construct()

    def generate_random_uuid(self):
        return str(uuid.uuid4())

    def generate_random_hex_str(self, length: int = 32) -> str:
        return "".join(random.choice("0123456789abcdef") for _ in range(length))

    def set_options_sets(self):
        options_sets_body = [
            "nlu_direct_response_filter",
            "deepleo",
            "disable_emoji_spoken_text",
            "responsible_ai_policy_235",
            "enablemm",
            "dv3sugg",
            "autosave",
            "iyxapbing",
            "iycapbing",
            "rai289",
            "enflst",
            "enpcktrk",
            "rcaldictans",
            "rcaltimeans",
            "eredirecturl",
        ]

        options_sets_by_styles = {
            "precise": options_sets_body
            + [
                "h3precise",
                "clgalileo",
                "gencontentv3",
            ],
            "balanced": options_sets_body
            + [
                "galileo",
                "saharagenconv5",
            ],
            "creative": options_sets_body
            + [
                "h3imaginative",
                "clgalileo",
                "gencontentv3",
            ],
        }
        self.options_sets = options_sets_by_styles[self.conversation_style]

    def set_search_options(self):
        self.plugins = []
        if self.enable_search:
            self.plugins.append({"id": "c310c353-b9f0-4d76-ab0d-1dd5e979cf68"})
        else:
            self.options_sets.append("nosearchall")

    def set_system_context(self):
        self.system_context = SystemPromptContextConstructor(
            self.system_prompt
        ).system_context

    def construct(self):
        self.set_options_sets()
        self.set_search_options()
        self.set_system_context()

        self.request_payload = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": self.options_sets,
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
                        "techpillscf",
                        "gbaa",
                        "gba",
                        "gbapa",
                        "codecreator",
                        "dlidcf",
                        "specedge",
                        "preall15",
                        "suppsm240-t",
                        "translref",
                        "ardsw_1_9_9",
                        "fluxnosearchc",
                        "fluxnosearch",
                        "1115rai289",
                        "1119backoss0",
                        "124multi2t",
                        "1129gpt4ts0",
                        "kchero50cf",
                        "cacfastapis",
                        "cacdupereccf",
                        "cacmuidarb",
                        "cacfrwebt2cf",
                        "sswebtop2cf",
                    ],
                    "verbosity": "verbose",
                    "scenario": "SERP",
                    "plugins": self.plugins,
                    "previousMessages": self.system_context,
                    "traceId": self.generate_random_hex_str(),
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
