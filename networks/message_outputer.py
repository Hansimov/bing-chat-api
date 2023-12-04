import json


class OpenaiStreamOutputer:
    """
    Create chat completion - OpenAI API Documentation
    * https://platform.openai.com/docs/api-reference/chat/create
    """

    def data_to_string(self, data={}, content_type="", media_type=None):
        # return (json.dumps(data) + "\n").encode("utf-8")
        data_str = f"{json.dumps(data)}\n"

        if media_type == "text/event-stream":
            data_str = f"data: {data_str}"

        return data_str

    def output(
        self,
        content=None,
        content_type=None,
        media_type=None,
    ) -> bytes:
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
            if content_type in ["InternalSearchQuery", "InternalSearchResult"]:
                content += "\n"
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
                    "delta": {},
                    "finish_reason": None,
                }
            ]
        return self.data_to_string(data, content_type, media_type)
