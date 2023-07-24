from .settings import Settings
from .parsing import ResponseParsing

class Search(ResponseParsing):

    def __init__(self, query=None):
        super().__init__()

    def image(self, query=None):
        url = Settings.URL_IMAGE.format(query) if query != None else Settings.URL_IMAGE.format("No image")
        html = self.parsing(url)
        self.data = []
        for image in html.find_all("a", attrs={"class": "img"}):
            # title = image["aria-label"]
            url = image.find("img")["data-src"]
            self.data.append(url)
        return self.data
