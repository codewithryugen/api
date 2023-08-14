import uvicorn
from fastapi import FastAPI

from Types import ShakoSchema
from yahoo_image import search
from otaku_news import otakunews
from shako_module import Shako
from anime import Gogoanime

HTTP_OK = 200
HTTP_ERR = 404
HTTP_ERR_SRV = 500

app = FastAPI()


@app.get("/")
def welcome():
    return {
        "status_code": HTTP_OK,
        "welcome": "api image"
        }

@app.get("/images/yahoo_image")
def image_yahoo(query: str):
    try:
        result = search.image(query)
        return {
            "status_code": HTTP_OK,
            "result": result
            }
    except:
        query = None
        return {
            "status_code": HTTP_ERR,
            "result": query
            }
            
# Shako api
@app.post("/shako/chat")
async def shako(data: ShakoSchema):
  try:
    prompt = data.prompt
    history = data.history
    chat_id = data.chat_id
    shako = Shako(prompt, history, chat_id)
    resolve, chat_id = await shako.resolve()
    return {
      "status_code": HTTP_OK,
      "responses": [
        {
          "chat_id": chat_id,
          "resolve": [resolve]
        }
      ]
    }
  except Exception as error:
    print(error)
    return {
      "status_code": HTTP_ERR,
      "message": "Failed resolve request"
    }

# Gogoanime api
@app.get("/gogoanime/recent")
def gogoanime_recent(page: str = None):
  try:
    gogo = Gogoanime()
    if not page:
      result = gogo.get_recent_release()
      return {
        "status_code": HTTP_OK,
        "responses": result
      }
    else:
      result = gogo.get_recent_release(page)
      return {
        "status_code": HTTP_OK,
        "responses": [result]
      }
  except Exception as error:
    return {
      "status_code": HTTP_ERR_SRV,
      "message": str(error)
    }

@app.get("/gogoanime/search")
def gogoanime_search(query: str):
    try:
        gogo = Gogoanime()
        result = gogo.search_anime(query)
        return {
            "status_code": HTTP_OK,
            "responses": result
        }

    except Exception as error:
        return {
            "status_code": HTTP_ERR_SRV,
            "message": str(error)
        }
        
@app.get("/gogoanime/details")
def gogoanime_details(query: str):
  try:
    gogo = Gogoanime()
    result = gogo.get_anime_details(query)
    print (result)
    return {
      "status_code": HTTP_OK,
      "responses": result
    }
  except Exception as error:
    print(error)
    return {
      "status_code": HTTP_ERR_SRV,
      "message": "Failed get anime data"
    }

@app.get("/gogoanime/list-episode")
def gogoanime_listeps(query: str):
  try:
    gogo = Gogoanime()
    result = gogo.get_episode_url(query)
    print (result)
    return {
      "status_code": HTTP_OK,
      "responses": result
    }
  except Exception as error:
    print(error)
    return {
      "status_code": HTTP_ERR_SRV,
      "message": "Failed get anime data"
    }
    
@app.get("/gogoanime/stream-url")
def gogoanime_stream(query: str):
  try:
    gogo = Gogoanime()
    result = gogo.get_stream_url(query)
    print (result)
    return {
      "status_code": HTTP_OK,
      "responses": result
    }
  except Exception as error:
    print(error)
    return {
      "status_code": HTTP_ERR_SRV,
      "message": "Failed get anime data"
    }

# Otaku News
@app.get("/news/otaku")
def news_otaku():
    try:
        data = otakunews.getNews()
        return {
            "status_code":HTTP_OK,
            "result":data
        }
        pass
    except:
        return {
            "status_code": HTTP_ERR,
            "result":"error"
        }
        pass
pass

if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")