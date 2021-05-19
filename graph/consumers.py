import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer


class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupname='dashboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )

        await self.accept()

        # for i in range(1000):
        #     await self.send(json.dumps({'value': randint(0,30)}))
        #     await sleep(1)

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )

    async def send_message(self, event):
        message = event['text']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            message
        ))
