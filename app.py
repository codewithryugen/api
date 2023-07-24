from flask import (
        Flask,
        request
    )
from flask_cors import CORS
from yahoo_image import search

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


if __name__ == "__main__":
    app.run(debug=True, port=3000)
