from utils.logger import logger
from networks import IdleOutputer


class MessageParser:
    def __init__(self, outputer=IdleOutputer()):
        self.delta_content_pointer = 0
        self.outputer = outputer

    def parse(self, data):
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
                    self.outputer.output(delta_content, message_type="Completions")
                    self.delta_content_pointer = len(content)
                    # Message: Suggested Questions
                    if message.get("suggestedResponses"):
                        logger.note("\nSuggested Questions: ")
                        for suggestion in message.get("suggestedResponses"):
                            suggestion_text = suggestion.get("text")
                            logger.file(f"- {suggestion_text}")
                        self.outputer.output(
                            message.get("suggestedResponses"),
                            message_type="Suggestions",
                        )
                # Message: Search Query
                elif message_type in ["InternalSearchQuery"]:
                    message_hidden_text = message["hiddenText"]
                    logger.note(f"\n[Searching: [{message_hidden_text}]]")
                    self.outputer.output(
                        message_hidden_text, message_type="InternalSearchQuery"
                    )
                # Message: Internal Search Results
                elif message_type in ["InternalSearchResult"]:
                    logger.note("[Analyzing search results ...]")
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
