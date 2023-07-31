import requests

body = {
  "prompt": "test"
}

res = requests.post("http://127.0.0.1:3000/shako/chat", json=body)
print(res.json())