import json
import requests
import random
import string

from datetime import datetime
from pathlib import Path
from utils.logger import logger


class CookiesConstructor:
    bypass_url = "https://zklcdc-pass.hf.space"

    def __init__(self):
        self.cookies = {}
        self.secrets_path = Path(__file__).parents[1] / "secrets.json"
        self.created_datetime_format = "%Y-%m-%d %H:%M:%S"

    def generate_kiev_rps_sec_auth(self):
        kiev = "".join(random.choices(string.ascii_uppercase + string.digits, k=32))
        return kiev

    def create_secrets_json(self):
        if not self.secrets_path.exists():
            self.secrets_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.secrets_path, "w") as wf:
                json.dump({}, wf)

    def is_local_cookies_valid(self):
        self.create_secrets_json()
        if self.secrets_path.exists():
            with open(self.secrets_path, "r") as f:
                secrets = json.load(f)
            if secrets.get("cookies"):
                cookies = secrets["cookies"]
                cookies_str = cookies.get("cookies_str")
                cookies_created_datetime = datetime.strptime(
                    cookies.get("created_time"), self.created_datetime_format
                )
                datetime_now = datetime.now()
                # if cookies created more than 12 hours, then it's invalid
                self.cookies_created_seconds = (
                    datetime_now - cookies_created_datetime
                ).seconds
                if self.cookies_created_seconds < 12 * 60 * 60:
                    self.cookies_str = cookies_str
                    self.cookies_created_datetime = cookies_created_datetime
                    return True
                else:
                    return False
        return False

    def requests_cookies(self):
        if self.is_local_cookies_valid():
            logger.success(
                f"Local Cookies Used: {self.cookies_created_datetime} "
                f"({round(self.cookies_created_seconds/60/60,2)} hours ago)"
            )
            return

        requests_body = {"cookies": ""}
        try:
            logger.note(f"Requesting Cookies from: {self.bypass_url}")
            res = requests.post(
                self.bypass_url,
                json=requests_body,
                timeout=15,
            )
            data = res.json()
            cookies_str = data["result"]["cookies"]
            cookies_screenshot = data["result"]["screenshot"]
            kiev = self.generate_kiev_rps_sec_auth()
            cookies_str = f"KievRPSSecAuth={kiev}; {cookies_str}"
            logger.note(f"Get Cookies: {cookies_str}")
            if cookies_str:
                with open(self.secrets_path, "r") as rf:
                    secrets = json.load(rf)
                secrets["cookies"] = {
                    "cookies_str": cookies_str,
                    "created_time": datetime.now().strftime(
                        self.created_datetime_format
                    ),
                    "screenshot": self.bypass_url + cookies_screenshot,
                }
                with open(self.secrets_path, "w") as wf:
                    json.dump(secrets, wf)
        except Exception as e:
            cookies_str = ""
            logger.err(e)

        self.cookies_str = cookies_str

    def cookies_str_to_dict(self):
        cookie_items = self.cookies_str.split(";")
        for cookie_item in cookie_items:
            if not cookie_item:
                continue
            cookie_key, cookie_value = cookie_item.split("=", 1)
            self.cookies[cookie_key.strip()] = cookie_value.strip()
        logger.success(f"Cookies: {self.cookies}")

    def construct(self):
        self.requests_cookies()
        self.cookies_str_to_dict()


if __name__ == "__main__":
    cookies_constructor = CookiesConstructor()
    cookies_constructor.construct()
