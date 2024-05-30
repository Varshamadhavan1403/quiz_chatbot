import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .reply_factory import generate_bot_responses, start_quiz_session

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope['session'].session_key

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

        # Start the quiz session when the connection is established
        start_quiz_session(self.scope['session'])
        bot_responses = generate_bot_responses('', self.scope['session'])
        for bot_response in bot_responses:
            self.send_message_to_group(bot_response, is_user=False)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_message = text_data_json['message']

        if user_message == '/reset':
            start_quiz_session(self.scope['session'])
            self.scope['session']['message_history'] = []
            self.scope['session'].save()
            bot_responses = generate_bot_responses('', self.scope['session'])
            for bot_response in bot_responses:
                self.send_message_to_group(bot_response, is_user=False)
            return

        self.send_message_to_group(user_message, is_user=True)

        bot_responses = generate_bot_responses(user_message, self.scope['session'])
        for bot_response in bot_responses:
            self.send_message_to_group(bot_response, is_user=False)

    def send_message_to_group(self, message, is_user):
        message_obj = {
            'type': 'chat_message',
            'is_user': is_user,
            'text': message
        }
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            message_obj
        )
        self.add_to_history(message_obj)

    def chat_message(self, message_obj):
        self.send(text_data=json.dumps(message_obj))

    def add_to_history(self, message_obj):
        message_history = self.scope['session'].get('message_history', [])
        message_history.append(message_obj)
        self.scope['session']['message_history'] = message_history
        self.scope['session'].save()
