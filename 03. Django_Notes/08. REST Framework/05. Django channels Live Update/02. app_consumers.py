import json
from channels.generic.websocket import AsyncWebsocketConsumer

class KeywordConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def update_keyword_status(self, event):
        status = event['status']
        # Send the status update to the client
        await self.send(text_data=json.dumps({'status': status}))
