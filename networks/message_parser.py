import json

from utils.logger import logger
from networks import IdleOutputer, ContentJSONOutputer


class MessageParser:
    def __init__(self, outputer=ContentJSONOutputer()):
        self.delta_content_pointer = 0
        self.outputer = outputer

    def parse(self, data, return_output=False):
        arguments = data["arguments"][0]
        if arguments.get("throttling"):
            throttling = arguments.get("throttling")
            # pprint.pprint(throttling)
        if arguments.get("messages"):
            for message in arguments.get("messages"):
                message_type = message.get("messageType")
                # Message: Displayed answer
                if message_type is None:
                    content = message["adaptiveCards"][0]["body"][0]["text"]
                    delta_content = content[self.delta_content_pointer :]
                    logger.line(delta_content, end="")
                    self.delta_content_pointer = len(content)
                    # Message: Suggested Questions
                    if message.get("suggestedResponses"):
                        logger.note("\nSuggested Questions: ")
                        for suggestion in message.get("suggestedResponses"):
                            suggestion_text = suggestion.get("text")
                            logger.file(f"- {suggestion_text}")
                    if return_output:
                        output_bytes = self.outputer.output(
                            delta_content, content_type="Completions"
                        )
                        if message.get("suggestedResponses"):
                            output_bytes += self.outputer.output(
                                message.get("suggestedResponses"),
                                content_type="SuggestedResponses",
                            )
                        return output_bytes

                # Message: Search Query
                elif message_type in ["InternalSearchQuery"]:
                    message_hidden_text = message["hiddenText"]
                    search_str = f"\n[Searching: [{message_hidden_text}]]"
                    logger.note(search_str)
                    if return_output:
                        return self.outputer.output(
                            search_str, content_type="InternalSearchQuery"
                        )
                # Message: Internal Search Results
                elif message_type in ["InternalSearchResult"]:
                    analysis_str = f"\n[Analyzing search results ...]"
                    logger.note(analysis_str)
                    if return_output:
                        return self.outputer.output(
                            analysis_str, content_type="InternalSearchResult"
                        )
                # Message: Loader status, such as "Generating Answers"
                elif message_type in ["InternalLoaderMessage"]:
                    # logger.note("[Generating answers ...]\n")
                    pass
                # Message: Internal thoughts, such as "I will generate my response to the user message"
                elif message_type in ["Internal"]:
                    pass
                # Message: Internal Action Marker, no value
                elif message_type in ["InternalActionMarker"]:
                    continue
                # Message: Render Cards for Webpages
                elif message_type in ["RenderCardRequest"]:
                    continue
                elif message_type in ["ChatName"]:
                    continue
                # Message: Not Implemented
                else:
                    raise NotImplementedError(
                        f"Not Supported Message Type: {message_type}"
                    )

        return (
            (
                json.dumps(
                    {
                        "content": "",
                        "content_type": "NotImplemented",
                    }
                )
            )
            + "\n"
        ).encode("utf-8")
