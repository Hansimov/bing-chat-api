import json


class OpenaiStreamOutputer:
    """
    Create chat completion - OpenAI API Documentation
    * https://platform.openai.com/docs/api-reference/chat/create
    """

    def data_to_string(self, data, content_type=""):
        # return (json.dumps(data) + "\n").encode("utf-8")
        data_str = f"data: {json.dumps(data)}\n"
        if content_type == "Finished":
            data_str += "data: [DONE]\n"
        return data_str

    def output(self, content=None, content_type=None) -> bytes:
        data = {
            "created": 1677825464,
            "id": "chatcmpl-bing",
            "object": "chat.completion.chunk",
            # "content_type": content_type,
            "model": "bing",
            "choices": [],
        }
        if content_type == "Role":
            data["choices"] = [
                {
                    "index": 0,
                    "delta": {"role": "assistant"},
                    "finish_reason": None,
                }
            ]
        elif content_type in [
            "Completions",
            "InternalSearchQuery",
            "InternalSearchResult",
            "SuggestedResponses",
        ]:
            data["choices"] = [
                {
                    "index": 0,
                    "delta": {"content": content},
                    "finish_reason": None,
                }
            ]
        elif content_type == "Finished":
            data["choices"] = [
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop",
                }
            ]
        else:
            data["choices"] = [
                {
                    "index": 0,
                    "delta": {"content": ""},
                    "finish_reason": None,
                }
            ]
        return self.data_to_string(data, content_type)
