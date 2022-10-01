import json
from asgiref.sync import async_to_sync
from .models import UserToUserConnection, User
from channels.generic.websocket import WebsocketConsumer
import time

class GroupChatConsumer(WebsocketConsumer):
    def connect(self):
        self.roomid = self.scope["url_route"]["kwargs"]["roomid"]
        self.room_group_name = f"chat_{self.roomid}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    # receive msg from ws

    def receive(self, text_data):
        data = json.loads(text_data)
        data["username"] = self.scope["user"].username # append username
        data["timestamp"] = time.time()
        print(data["timestamp"])
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "data": data
            }
        )
    
    def chat_message(self, event):
        self.send(text_data=json.dumps(event["data"]))

class UUChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.u1 = self.scope["url_route"]["kwargs"]["u1"]
        self.u2 = self.scope["url_route"]["kwargs"]["u2"]
        
        both = [self.u1, self.u2]
        if self.scope["user"].username not in both:
            print("not authorized")
            self.close() # you aren't authorized
        both.sort()
        self.room_group_name = f"chat_{both[0]}__{both[1]}"

        try:
            self.u1 = User.objects.get(username=self.u1)
            self.u2 = User.objects.get(username=self.u2)
        except Exception as e:
            print(e)
            print("user doesn't exist")
            self.close(code=4001) # user doesn't exist

        try:
            uu = UserToUserConnection.objects.get(u1=self.u1, u2=self.u2)
            print("uu already exists")
            self.close()
        except:
            UserToUserConnection.objects.create(u1=self.u1, u2=self.u2)
            print("uu created")
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
        self.accept()

    def disconnect(self, close_code):
        try:
            uu = UserToUserConnection.objects.get(u1=self.u1, u2=self.u2)
            uu.delete()
        except:
            uu = UserToUserConnection.objects.filter(u1=self.u1, u2=self.u2)
            uu.delete()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "close",
            }
        )
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    # receive msg from ws

    def receive(self, text_data):
        data = json.loads(text_data)
        data["username"] = self.scope["user"].username # append username
        data["timestamp"] = time.time()
        print(data["timestamp"])
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "data": data
            }
        )
    
    def chat_message(self, event):
        self.send(text_data=json.dumps(event["data"]))
    def close(self, event):
        self.send(text_data=json.dumps({"close": "yes"}))