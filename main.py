from conversations import ConversationSession

if __name__ == "__main__":
    prompts = [
        "Today's weather of California",
        "Please summarize your previous answer in table format",
    ]
    with ConversationSession("precise") as session:
        for prompt in prompts:
            session.chat(prompt)
