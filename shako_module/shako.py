import websockets

from uuid import uuid4
from base64 import urlsafe_b64encode
from json import dumps, loads
from uuid import uuid4


class Shako:
  
  def __init__(self, prompt, history = [] , chat_id = None):
    self.history = history
    self.prompt = prompt
    
    self.websocket = None
    self.chat_id = chat_id
    self.uri = 'wss://api.shako.ai/api/chat'
    self.headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
      'Sec-WebSocket-Version': '13',
      'Origin': 'https://shako.ai',
      'Sec-WebSocket-Extensions': 'permessage-deflate',
      'Sec-WebSocket-Key': self.web_key(),
      'Connection': 'Upgrade',
    }
    
  def web_key(safe):
    return urlsafe_b64encode(uuid4().bytes).decode("utf-8")
  
  async def process_response(self, res):
    result = ''
    while True:
      response_data = loads(res)
      content = response_data.get("content")
      if content:
        result += content
      response_types = response_data.get("type")
      if response_types == "end":
        break
      res = await self.websocket.recv()
    return result.strip(), response_data.get("chat_id")
  
  async def send_initial_data(self, initial_data):
    await self.websocket.send(dumps(initial_data))
    response = await self.websocket.recv()
    result, chat_id = await self.process_response(response)
    return result, chat_id
  
  async def initial_data(self, query):
    data = {
      "chat_id": str(uuid4()) if self.chat_id is None else self.chat_id,
      "metadata": {},
      "prompt": self.history + [{'content': query, 'role': 'user'}]
    }
    return data
  
  async def resolve(self):
    initial_data = await self.initial_data(self.prompt)
    async with websockets.connect(self.uri, extra_headers=self.headers) as self.websocket:
      result, chat_id = await self.send_initial_data(initial_data)
      
      response = [
        {
          "role": "user", "content": self.prompt,
          "role": "model", "content": result
        }
      ]
    return response, chat_id