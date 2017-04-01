from json import dumps, loads
from pprint import pprint
from bot_email.emailbot import Email
from bot_services.user_service import UserService
import requests
import facebook

# Permanent page access token
# TODO change access token to production one before pushing.
PAGE_ACCESS_TOKEN = 'EAAFJaTQTZCAgBAKquTNCRxUz2edEmSuocZC9EreThZAiGFImZAHGGqVlcLdvRDe3vMNXZBvXnQL3ZC0VMJY8IMAWt6t0j8tZCBwsYBZAQDEYOh1kwdjzmnu6zkg1tPyWITWTtgcQvZAw0mvyqZAIkZABmmkMQr1UQwBCkKkcXCTmaZAFHAZDZD'
# PAGE_ACCESS_TOKEN = 'EAAVTNRkgcFgBAAj8hRodXNlJ5Lf27hqRLUyyZBfrPLyBx9Edp91MRGzHaZCUUw34hpZCAV4hCAwwZAEKtzpFh7f8X53h6JnDzTFZAQbY00ohzs5RD9fFoZA2XCPhxFxZAYimeQonAUpcd1wkOK8HkdcGZCoeFVqc7T3JzcnYGBVeLgZDZD'
graph = facebook.GraphAPI(PAGE_ACCESS_TOKEN, version='2.2')

class CommunicationService:
    def get_user_info(user_id):
        user = requests.get(("https://graph.facebook.com/v2.6/%s?access_token=%s" % (user_id, PAGE_ACCESS_TOKEN)))
        return user

    def post_facebook_message(fbid, received_message):
        # TODO Change access token
        post_message_url = 'https://graph.facebook.com/v2.8/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
        response_msg = dumps({"recipient":{"id":fbid}, "message":{"text":received_message}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
        print('SEND STATUS')
        pprint(status.json())

    def post_facebook_message_to_all(received_message):
        for user in UserService.getAllUsers():
            CommunicationService.post_facebook_message(user.user_id,received_message)

    def post_facebook_message_to_class(students_in_class, received_message):
        for user in students_in_class:
            CommunicationService.post_facebook_message(user.user_id,received_message)

    def get_event_info(event_id):
        event = requests.get(("https://graph.facebook.com/v2.6/%s/?fields=category%%2Cname%%2Cend_time&access_token=%s" % (event_id, PAGE_ACCESS_TOKEN)))
        if (event.ok):
            return event
        raise Exception('event does not exist')
