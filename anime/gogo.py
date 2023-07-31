"""
BEGIN
Class of Gogoanime secwawer <- Kawai name UwU
I hove senpai liked UwU
  - Requirements
      - bs4
      - requests
      - lxml
      
  - To-Do
    - get_anime_details: completed
    - search_anime: completed
    - get_episode_url: completed
    - get_recent_release: completed
    - get_stream_url: completed
END
"""



import re
import requests

from bs4 import BeautifulSoup
from anime.classes import PlaylistParser
from anime.classes import streamExtractor


class Gogoanime:
  
  def __init__(self, root_url = "https://gogoanime.cl"):
    self.root_url = root_url
  
  def get_anime_details(self, category_url: str):
    """
    Get anime information and description
      - param:
          - category_url -> str: Url category example: https://gogoanime.cl/category/oniichan-wa-oshimai-uncensored
       - return -> list:
          - season: Season of anime
          - synopsis: Synopsis anime
          - released: Released year of anime
          - status: ongoing, completed, finished
          - image_url: image cover anime
    """
    try:
      req = self.__get(category_url)
      soup = BeautifulSoup(req.text, "lxml")
      anime_info_body = soup.find("div", {"class": "anime_info_body_bg"})
      image_url = anime_info_body.find("img")["src"]
      etc = anime_info_body.find_all("p", {"class": "type"})
      
      title = anime_info_body.find("h1").text.strip()
      season = etc[0].text.replace("\n", "").replace("Type: ", "")
      synopsis = etc[1].text.replace("\n", "")
      
      genres = [
          x["title"]
          for x in BeautifulSoup(str(etc[2]), "lxml").find_all("a")
      ]
      released = etc[3].text.replace("Released: ", "")
      status = etc[4].text.replace("\n", "").replace("Status: ", "")
      
      return {
        "title": title,
        "image_url": image_url,
        "season": season,
        "synopsis": synopsis,
        "genres": genres,
        "released": released,
        "status": status
      }
    except Exception as ewwow:
      return ewwow
      
  
  def search_anime(self, titles: str):
    """
    Get anime info
    param: title -> str: Name of anime to search
    return list []
    """
    try:
      results = []
      res = self.__get(f"https://ajax.gogo-load.com/site/loadAjaxSearch?keyword={titles}")
      if res:
        title = [_.group(1) for _ in re.finditer(r"<\\/div>(.*?)<\\/a><\\/div>", res.text)]
        url = [_.group(1) for _ in re.finditer(r"<a href=\\\"(.*?)\\\" ", res.text)]
        picture = [_.group(1) for _ in re.finditer(r"style='background:\surl[\(']\\(.*?)[\)']", res.text)]
        
        for indx, dta in enumerate(title):
          title = dta.replace(r"\/", "/")
          catagory_url = url[indx].replace(r"\/", "/")
          catagory_url = f"{self.root_url}/{catagory_url}"
          picture_url = picture[indx].replace(r"\/", "/").replace(r'"', "")[:-1]
          
          results.append({
            "titles": title,
            "catagory_url": catagory_url,
            "picture_url": picture_url
          })
        
        return results
    except Exception as error:
      return error
  
  def get_episode_url(self, catagory_url: str):
    """
    Grab all data episode of anime 
    - param: 
        - catagory_url -> str: Url category example: https://gogoanime.cl/category/oniichan-wa-oshimai-uncensored
    - return -> List: List all episode of anime
    """
    try:
      episode = []
      req = self.__get(catagory_url)
      id = re.search(r'<input.+?value="(\d+)" id="movie_id"', req.text).group(1)
      req = self.__get(f"https://ajax.gogo-load.com/ajax/load-list-episode", {"ep_start": 0, "ep_end": 9999, "id": id})
      soup = BeautifulSoup(req.content, "lxml")
      eps_url = soup.find_all("a")
      
      for i in eps_url:
        episode.append(f"{self.root_url}{i.get('href').strip()}")
      episode.reverse()
      return episode
    except Exception as error:
      return error
    
  
  def get_stream_url(self, episode_url: str):
    """
    Get stream url
    - params
        - episode_url -> str: Episode url of anime.
                              Example: https://gogoanime.cl/oniichan-wa-oshimai-episode-1
    - return:
    """
    playlist = PlaylistParser()
    url_excractor = streamExtractor()
    stream_url = url_excractor.extract(episode_url)
    
    results = playlist.parser(stream_url)
    return results
  
  
  def get_recent_release(self, page=1):
    try:
      recent_list = []
      req = self.__get(f"https://ajax.gogo-load.com/ajax/page-recent-release.html?page={page}").text
      regex = r"<li>\s*\n.*\n.*<a\shref=[\"'](?P<href>.*?-episode-(?P<episode>\d+))[\"']\s*title=[\"'](?P<title>.*?)[\"']>\n.*<img\ssrc=[\"'](?P<img>.*?)[\"']"
      
      if req:
        matches = list(re.findall(regex, req, re.MULTILINE))
        for match in matches:
          recent_list.append({
            "title": match[2],
            "lastest_episode": int(match[1]),
            "lastest_episode_url": f"{self.root_url}{match[0]}",
            "picture_url": match[3]
          })
      return recent_list
    except Exception as error:
      return error
  
  def __get(self, url, params = None):
    req = requests.get(url, params=params)
    return req
  
  def __post(self, url, body):
    req = requests.post(url, json=body)
    return req