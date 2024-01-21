import re
from pprint import pprint


class MessageComposer:
    def __init__(self):
        pass

    def merge(self, messages, suffix=True) -> str:
        self.messages = messages
        self.merged_str = ""
        self.merged_str_list = []
        self.system_prompt = ""
        self.system_prompt_list = []

        assistant_messages = [
            message for message in messages if message["role"] not in ["user", "system"]
        ]
        if len(assistant_messages) <= 0:
            for message in messages:
                role = message["role"]
                content = message["content"]
                if role.lower() in ["system"]:
                    self.system_prompt += content
                if role.lower() in ["user"]:
                    self.merged_str_list.append(content)
        else:
            for message in messages:
                role = message["role"]
                content = message["content"]

                if role.lower() in ["system"]:
                    self.system_prompt_list.append(content)
                    continue
                if role.lower() in ["user"]:
                    role_str = "me"
                elif role.lower() in ["assistant", "bot"]:
                    role_str = "you"
                else:
                    role_str = "unknown"
                self.merged_str_list.append(f"`{role_str}`:\n{content}")

            if suffix:
                self.merged_str_list.append("`you`:")

        self.merged_str = "\n\n".join(self.merged_str_list)
        self.system_prompt = "\n\n".join(self.system_prompt_list)

        return self.merged_str

    def split(self, merged_str) -> list:
        self.messages = []
        self.merged_str = merged_str
        pattern = r"`(?P<role>me|you)`:\n(?P<content>.*)\n+"
        matches = re.finditer(pattern, self.merged_str, re.MULTILINE)
        matches_list = list(matches)
        if len(matches_list) <= 0:
            self.messages = [
                {
                    "role": "user",
                    "content": self.merged_str,
                }
            ]
        else:
            for match in matches_list:
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
