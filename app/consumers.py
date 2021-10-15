import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Thread, Message , User , UserProfile

@database_sync_to_async
def get_thread(id):
    return Thread.objects.get(id=id).id

@database_sync_to_async
def save_message(message,thread_id,sender):
    thread = Thread.objects.get(id=thread_id)
    Message.objects.create(thread=thread,sender=sender, message=message)
    return True

@database_sync_to_async
def user_status(message,sender):
    user = User.objects.get(username=sender)
    user.userprofile.is_online = True if message == 'Online' else False
    user.userprofile.save()
    return True

# chat consumer
class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.thread = await get_thread(self.scope['url_route']['kwargs']['id'])
        self.chat_room = f"room_{self.thread}"
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data is not None:
            message = data.get('message')
            response = {
                'message': message,
                'user':self.scope['user'].username,
            }
            await self.channel_layer.group_send(
            self.chat_room,
                {
                    "type": "send_json",
                    "text": json.dumps(response)
                }
            )
            await save_message(message,self.thread,self.scope['user'])


    async def disconnect(self,event):
        print("Event Running",event)


class StatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.chat_room = "status"
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data is not None:
            message = data.get('message')
            response = {
                'message': message,
                'user':self.scope['user'].username,
            }
            print(response)
            await self.channel_layer.group_send(
            self.chat_room,
                {
                    "type": "send_json",
                    "text": json.dumps(response)
                }
            )
            await user_status(message,self.scope['user'])


    async def disconnect(self,event):
        print("Event Running",event)
        response = {
            'message': "Offline",
            'user':self.scope['user'].username,
        }
        print(response)
        await self.channel_layer.group_send(
        self.chat_room,
            {
                "type": "send_json",
                "text": json.dumps(response)
            }
        )
        await user_status('Offline',self.scope['user'])


