class CookiesConstructor:
    def __init__(self) -> None:
        self.cookies_list = []  # Dumped from Cookie-Editor extension in Browser

    def construct(self):
        self.cookies = {}
        for cookie in self.cookies_list:
            self.cookies[cookie["name"]] = cookie["value"]
