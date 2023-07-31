from flask import (
        Flask,
        request
    )
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS


from yahoo_image import search
from otaku_news import otakunews
from shako_module import Shako
from anime import Gogoanime

HTTP_OK = 200
HTTP_ERR = 404
HTTP_ERR_SRV = 500

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

""" 
Setup swagger ui for documentation
"""
blueprint_swagger = get_swaggerui_blueprint(
  "/docs",
  "/static/swagger.yaml",
  config = {
    "app_name": "RestAPI"
  }
)

app.register_blueprint(blueprint_swagger)

""" 
END
"""

@app.route("/", methods=["GET"])
def welcome():
    return {
        "status_code": HTTP_OK,
        "welcome": "api image"
        }

@app.route("/images/yahoo_image", methods=["GET"])
def image_yahoo():
    try:
        query = request.args["q"]
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
@app.route("/shako/chat", methods=["post"])
async def shako():
  try:
    data = request.json
    prompt = data.get("prompt")
    history = data.get("history", [])
    chat_id = data.get("chat_id", None)
    
    if not prompt or not data:
      return {
        "status_code": HTTP_ERR,
        "message": "invalid request. missing prompt on body request"
      }
    else:
      
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
@app.route("/gogoanime/recent", methods=["get"])
def gogoanime_recent():
  try:
    page = request.args.get("page", "")
    gogo = Gogoanime()
    if page is None or page == "":
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

@app.route("/gogoanime/search", methods=["get"])
def gogoanime_search():
    try:
        query = request.args.get("query", "")
        if not query:
            return {
                "status_code": HTTP_ERR,
                "message": "Missing 'query' parameter. Please add 'query' in the parameters."
            }

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
        
@app.route("/gogoanime/details", methods=["get"])
def gogoanime_details():
  try:
    query = request.args.get("query")
    if not query:
        return {
          "status_code": HTTP_ERR,
          "message": "Missing 'query' parameter. Please add 'query' in the parameters."
        }
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

@app.route("/gogoanime/list-episode", methods=["get"])
def gogoanime_listeps():
  try:
    query = request.args.get("query")
    if not query:
        return {
          "status_code": HTTP_ERR,
          "message": "Missing 'query' parameter. Please add 'query' in the parameters."
        }
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
    
@app.route("/gogoanime/stream-url", methods=["get"])
def gogoanime_stream():
  try:
    query = request.args.get("query")
    if not query:
        return {
          "status_code": HTTP_ERR,
          "message": "Missing 'query' parameter. Please add 'query' in the parameters."
        }
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
@app.route("/news/otaku",methods=["GET"])
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
    app.run(debug=True, port=3000)
