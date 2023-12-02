import json


class IdleOutputer:
    def output(self, content=None, content_type=None):
        return json.dumps({}).encode("utf-8")


class ContentJSONOutputer:
    def output(self, content=None, content_type=None):
        return (
            json.dumps(
                {
                    "content": content,
                    "content_type": content_type,
                }
            )
            + "\n"
        ).encode("utf-8")
