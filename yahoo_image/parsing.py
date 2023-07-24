from bs4 import BeautifulSoup as parser
from requests import Session
from .settings import Settings

class ResponseParsing(Session):
    headers = {
        "User-Agent": Settings.USER_AGENT
    }

    def __init__(self):
        super().__init__()

    def get_url(self, url):
        return self.get(url)

    def parsing(self, url):
        return parser(self.get_url(url).text, "html.parser")
