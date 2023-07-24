#!/usr/bin/python3
from bs4 import BeautifulSoup as Bs
from requests import get

class OtakuNews:
    def __init__(self):
        self.base_url = "https://www.otakunews.com"

    def getData(self, html):
        soup = Bs(html, 'html.parser')
        articles = soup.find_all('h2')
        index = 0
        data_list = []
        for article in articles:
            title = article.text
            link_title = self.base_url+article.a['href']
            detail = soup.find_all('span',{'class','articleDetails'})[index].text
            category = soup.find_all('p',{'class','categoryDetails'})[index].text
            paragraph = soup.find_all('p',None)[index].text
            data = {
                "title":title,
                "link_title":link_title,
                "detail":detail,
                "category":category,
                "paragraph":paragraph
            }
            data_list.append(data)
            index += 1
        return data_list

    def getNews(self):
        html = get(self.base_url).text
        data = self.getData(html)
        return data

