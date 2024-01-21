import json
from utils.logger import logger
from networks import OpenaiStreamOutputer


class MessageParser:
    def __init__(self, outputer=OpenaiStreamOutputer()):
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
                    # content = message["adaptiveCards"][0]["body"][0]["text"]
                    content = message["text"]
                    delta_content = content[self.delta_content_pointer :]
                    logger.line(delta_content, end="")
                    self.delta_content_pointer = len(content)
                    # Message: Suggested Questions
                    if message.get("suggestedResponses"):
                        logger.note("\nSuggested Questions: ")
                        suggestion_texts = [
                            suggestion.get("text")
                            for suggestion in message.get("suggestedResponses")
                        ]
                        for suggestion_text in suggestion_texts:
                            logger.file(f"- {suggestion_text}")
                    if return_output:
                        completions_output = self.outputer.output(
                            delta_content, content_type="Completions"
                        )
                        if message.get("suggestedResponses"):
                            suggestions_output = self.outputer.output(
                                suggestion_texts,
                                content_type="SuggestedResponses",
                            )
                            return [completions_output, suggestions_output]
                        else:
                            return completions_output
                # Message: Search Query
                elif message_type in ["InternalSearchQuery"]:
                    search_query_str = message.get("hiddenText")
                    if return_output:
                        # output_str = self.outputer.output(
                        #     search_query_str, content_type="InternalSearchQuery"
                        # )
                        # logger.note(output_str)
                        # return output_str
                        return None
                # Message: Internal Search Results
                elif message_type in ["InternalSearchResult"]:
                    if message.get("groundingInfo"):
                        web_search_results = message.get("groundingInfo").get(
                            "web_search_results"
                        )
                        invocation = message.get("invocation")
                        if return_output:
                            search_results_str = self.outputer.output(
                                {
                                    "invocation": invocation,
                                    "web_search_results": web_search_results,
                                },
                                content_type="InternalSearchResult",
                            )
                            data = json.loads(search_results_str)
                            logger.note(data["choices"][0]["delta"]["content"])
                            return search_results_str
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

        return None
