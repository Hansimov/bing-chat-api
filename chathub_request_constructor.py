import random
import uuid
from datetime import datetime


def generate_random_hex_str(length: int = 32) -> str:
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


def generate_random_uuid():
    return str(uuid.uuid4())


def get_locale():
    return "en-US"


def get_timestamp_str():
    now = datetime.now()
    now_utc = datetime.utcnow()
    timezone_offset = now - now_utc
    offset_seconds = timezone_offset.total_seconds()
    offset_hours = int(offset_seconds // 3600)
    offset_minutes = int((offset_seconds % 3600) // 60)
    offset_string = f"{offset_hours:+03d}:{offset_minutes:02d}"
    timestamp_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + offset_string
    # print(timestamp_str)
    return timestamp_str


def get_prompt():
    return "Hello, who are you?"


class ChathubRequestConstructor:
    def __init__(
        self,
        conversation_style: str,
        client_id: str,
        conversation_id: str,
        invocation_id: int = 0,
    ):
        self.client_id = client_id
        self.conversation_id = conversation_id
        self.message_id = generate_random_uuid()
        self.invocation_id = invocation_id
        self.conversation_style = conversation_style
        self.construct()

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
                    "traceId": generate_random_hex_str(),
                    "conversationHistoryOptionsSets": [
                        "autosave",
                        "savemem",
                        "uprofupd",
                        "uprofgen",
                    ],
                    "isStartOfSession": self.invocation_id == 0,
                    "requestId": self.message_id,
                    "message": {
                        "locale": get_locale(),  # "en-US"
                        "market": get_locale(),  # "en-US"
                        "region": get_locale()[-2:],  # "US"
                        "location": "lat:47.639557;long:-122.128159;re=1000m;",
                        "locationHints": [
                            {
                                "SourceType": 1,
                                "RegionType": 2,
                                "Center": {
                                    "Latitude": 38.668399810791016,
                                    "Longitude": -121.14900207519531,
                                },
                                "Radius": 24902,
                                "Name": "Folsom, California",
                                "Accuracy": 24902,
                                "FDConfidence": 0.5,
                                "CountryName": "United States",
                                "CountryConfidence": 8,
                                "Admin1Name": "California",
                                "PopulatedPlaceName": "Folsom",
                                "PopulatedPlaceConfidence": 5,
                                "PostCodeName": "95630",
                                "UtcOffset": -8,
                                "Dma": 862,
                            }
                        ],
                        "userIpAddress": "192.55.55.51",
                        "timestamp": get_timestamp_str(),  # "2023-11-20T12:50:17+08:00",
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": get_prompt(),
                        "messageType": "Chat",
                        "requestId": self.message_id,  # "a6ecd3aa-1007-6959-52fb-9e23f34e86be",
                        "messageId": self.message_id,  # "a6ecd3aa-1007-6959-52fb-9e23f34e86be",
                    },
                    "tone": self.conversation_style.capitalize(),
                    "spokenTextMode": "None",
                    "conversationId": self.conversation_id,  # "51D|BingProd|30FA137663F2BDBA514A0F31EE0A99E082B5AF8C0DA05696D2A5C6B56C10CF99",
                    "participant": {
                        "id": self.client_id,  # "1055519195774559",
                    },
                }
            ],
            "invocationId": str(self.invocation_id),
            "target": "chat",
            "type": 4,
        }
