import cssutils
import re
from bs4 import BeautifulSoup
from DrissionPage import WebPage, ChromiumOptions
from pprint import pprint


class ProxyRowExtractor:
    def __init__(self):
        pass

    def extract(self, table_html):
        soup = BeautifulSoup(table_html, "html.parser")
        rows = soup.find_all("tr")
        keys = [
            "ip",
            "port",
            "check_datetime_and_interval",
            "bandwidth_and_latency",
            "stability_and_samples",
            "country",
            "anonymity",
        ]
        row_dicts = []
        for row in rows:
            row_dict = {}
            cells = row.find_all("td")
            for key, cell in zip(keys, cells):
                cell_text = re.sub(r"\s+", " ", cell.text.strip())
                if key == "bandwidth_and_latency":
                    progress_bar = cell.find("div", class_="progress-bar-inner")
                    bandwidth = cssutils.parseStyle(progress_bar["style"])["width"]
                    latency = cell_text
                    row_dict["bandwidth"] = bandwidth
                    row_dict["latency"] = latency
                elif key == "check_datetime_and_interval":
                    check_datetime = cell.find("time").attrs["datetime"]
                    check_interval = cell_text
                    row_dict["check_datetime"] = check_datetime
                    row_dict["check_interval"] = check_interval
                elif key == "stability_and_samples":
                    res = re.match(r"(\d+%)\s*\((\d+)\)", cell_text)
                    stability = res.group(1)
                    samples = res.group(2)
                    row_dict["stability"] = stability
                    row_dict["samples"] = samples
                else:
                    row_dict[key] = cell_text
            pprint(row_dict)
            row_dicts.append(row_dict)


class ProxyScanner:
    def __init__(self, scan_proxy=None):
        self.scan_proxy = scan_proxy
        self.init_proxy_servers()

    def init_proxy_servers(self):
        # https://www.proxynova.com/proxy-server-list
        self.proxy_server_list_url_base = (
            "https://www.proxynova.com/proxy-server-list/country"
        )
        countries = ["ar", "br", "co", "de", "id", "in", "mx", "sg", "us"]
        self.proxy_server_list_urls = [
            f"{self.proxy_server_list_url_base}-{country}" for country in countries
        ]

    def run(self):
        proxy_url = self.proxy_server_list_urls[-1]
        options = ChromiumOptions()
        options.set_argument("--incognito")
        options.set_argument(f"--proxy-server", self.scan_proxy)
        self.options = options
        page = WebPage(driver_or_options=self.options)
        page.get(proxy_url)
        print(page.title)
        page.wait.ele_display("#tbl_proxy_list")
        ele = page.ele("#tbl_proxy_list")
        # print(ele.html)
        extractor = ProxyRowExtractor()
        extractor.extract(ele.html)

        self.page = page


if __name__ == "__main__":
    scanner = ProxyScanner(scan_proxy="http://localhost:11111")
    scanner.run()
