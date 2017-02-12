from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests

from json import dumps, loads
from pprint import pprint

PAGE_ACCESS_TOKEN = 'EAATYvrVIHsIBADoFlddL8Aqeu9YiXCkzBehGuqGBzsl2dM22QTvsNH2AuBpkaWPGfnIifWDNJYUlhbo7E8M15amsnBDtZBZC1WFohgYVg5HJ2zA1vKZBOthJZBwQPbX6TzMSpOfXCQxfrbPMjyh40nC5o6yQBm1xDpBpIvlKxwZDZD'

def post_facebook_message(fbid, recevied_message):
    # TODO Change access token           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    response_msg = dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Create your views here.
class McBotView(generic.View):
    def get(self, request, *args, **kwargs):
        # TODO Change the verify_token
        if self.request.GET['hub.verify_token'] == '2318934571':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])      
        return HttpResponse()


