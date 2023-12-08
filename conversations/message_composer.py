import re
from pprint import pprint


class MessageComposer:
    def __init__(self):
        pass

    def merge(self, messages) -> str:
        self.messages = messages
        self.merged_str = ""
        for message in messages:
            role = message["role"]
            if role.lower() in ["system", "user"]:
                role_str = "me"
            elif role.lower() in ["assistant", "bot"]:
                role_str = "you"
            else:
                role_str = "unknown"
            content = message["content"]
            self.merged_str += f"`{role_str}`:\n{content}\n\n"
        self.merged_str += "`you`:\n"
        return self.merged_str

    def split(self, merged_str) -> list:
        self.messages = []
        self.merged_str = merged_str
        pattern = r"`(?P<role>me|you)`:\n(?P<content>.*)\n+"
        matches = re.finditer(pattern, self.merged_str, re.MULTILINE)
        for match in matches:
            role = match.group("role")

            if role == "me":
                role_str = "user"
            elif role == "you":
                role_str = "assistant"
            else:
                role_str = "unknown"

            self.messages.append(
                {
                    "role": role_str,
                    "content": match.group("content"),
                }
            )
        return self.messages


if __name__ == "__main__":
    composer = MessageComposer()
    messages = [
        {
            "role": "system",
            "content": "You are a LLM developed by OpenAI. Your name is GPT-4.",
        },
        {"role": "user", "content": "Hello, who are you?"},
        {"role": "assistant", "content": "I am a bot."},
        {"role": "user", "content": "What is your name?"},
        {"role": "assistant", "content": "My name is Bing."},
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": "What is a robot's favorite type of music?"},
        {
            "role": "user",
            "content": "How many questions have I asked? Please list them.",
        },
    ]
    merged_str = composer.merge(messages)
    print(merged_str)
    pprint(composer.split(merged_str))
    print(composer.merge(composer.split(merged_str)))
