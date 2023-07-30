from flask import (
        Flask,
        request
    )
from flask_cors import CORS
from yahoo_image import search
from otaku_news import otakunews
from shako_module import Shako

HTTP_OK = 200
HTTP_ERR = 404

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
