class ConversationCreateHeadersConstructor:
    def __init__(self):
        self.construct()

    def construct(self):
        self.request_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Referer": "https://www.bing.com/search?q=Bing+AI&showconv=1&setlang=en&cc=us",
            "X-Ms-Useragent": "azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.12.0 OS/Windows",
            "X-Forwarded-For": "65.49.22.66",
        }
