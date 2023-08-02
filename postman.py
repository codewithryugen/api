import requests

URL = "http://127.0.0.1:3000"

body = {
  "prompt": "test"
}

print("Test shako chat ...")
res = requests.post(f"{URL}/shako/chat", json=body)
print(res.json())
print()
print("Test gogoanime recent ...")
gogo_recent = requests.get(f"{URL}/gogoanime/recent")
print(gogo_recent.json())
print()
print("Test gogoanime search ...")
gogo_srch = requests.get(f"{URL}/gogoanime/search?query=onimai")
print(gogo_srch.json())
print()
print("Test gogoanime information ...")
gogo_info = requests.get(f'{URL}/gogoanime/details?query=https://gogoanime.cl/category/oniichan-wa-oshimai')
print(gogo_info.json())
print()
print("Test gogoanime list eps ...")
gogo_info = requests.get(f'{URL}/gogoanime/list-episode?query=https://gogoanime.cl/category/oniichan-wa-oshimai')
print(gogo_info.json())
print()
print("Test gogoanime stream url ...")
gogo_info = requests.get(f'{URL}/gogoanime/stream-url?query=https://gogoanime.cl/oniichan-wa-oshimai-episode-1')
print(gogo_info.json())
print()