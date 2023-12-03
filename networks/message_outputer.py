import json


class OpenaiStreamOutputer:
    def output(self, content=None, content_type=None) -> bytes:
        return (
            json.dumps(
                {
                    "content": content,
                    "content_type": content_type,
                }
            )
            + "\n"
        ).encode("utf-8")
