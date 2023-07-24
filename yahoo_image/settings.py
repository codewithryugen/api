from dataclasses import dataclass 

@dataclass
class Settings:
    BASE_URL: str = "https://search.yahoo.com/search/"
    URL_IMAGE: str = BASE_URL + "images?p={}"
    USER_AGENT: str = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
