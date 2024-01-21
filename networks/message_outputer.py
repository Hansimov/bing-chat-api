import json
import re


class OpenaiStreamOutputer:
    """
    Create chat completion - OpenAI API Documentation
    * https://platform.openai.com/docs/api-reference/chat/create
    """

    def data_to_string(self, data={}, content_type=""):
        # return (json.dumps(data) + "\n").encode("utf-8")
        data_str = f"{json.dumps(data)}"

        return data_str

    def output(self, content=None, content_type=None) -> str:
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
        elif content_type == "Completions":
            data["choices"] = [
                {
                    "index": 0,
                    "delta": {"content": content},
                    "finish_reason": None,
                }
            ]
        elif content_type == "InternalSearchQuery":
            search_str = f"Searching: [**{content.strip()}**]\n"
            data["choices"] = [
                {
                    "index": 0,
                    "delta": {"content": search_str},
                    "finish_reason": None,
                }
            ]
        elif content_type == "InternalSearchResult":
            invocation = content["invocation"]
            web_search_results = content["web_search_results"]
            matches = re.search('\(query="(.*)"\)', invocation)
            if matches:
                search_query = matches.group(1)
            else:
                search_query = invocation
            search_str = f"Searching: [**{search_query.strip()}**]"
            search_results_str_list = []
            for idx, search_result in enumerate(web_search_results):
                search_results_str_list.append(
                    f"{idx+1}. [{search_result['title']}]({search_result['url']})"
                )
            search_results_str = "\n".join(search_results_str_list)
            search_results_str = (
                f"<details>\n"
                f"<summary>\n{search_str}\n</summary>\n"
                f"{search_results_str}\n"
                f"</details>\n"
            )
            data["choices"] = [
                {
                    "index": 0,
                    "delta": {"content": search_results_str},
                    "finish_reason": None,
                }
            ]
        elif content_type == "SuggestedResponses":
            suggestion_texts_str = "\n\n---\n\n**Suggested Questions:**\n"
            suggestion_texts_str += "\n".join(f"- {item}" for item in content)
            data["choices"] = [
                {
                    "index": 0,
                    "delta": {"content": suggestion_texts_str},
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
        return self.data_to_string(data, content_type)
