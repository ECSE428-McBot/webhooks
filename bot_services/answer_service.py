import re
from bot_services.user_service import UserService, Question
from bot_services.communication_service import CommunicationService
from bot_services.authentication_service import AuthenticationService
from bot_services.event_service import EventService
from bot_services.calendar_service import CalendarService

MSG_ASK_FOR_USER_TYPE = 'Are you a [student] or [instructor]?'
QUESTION_USER_TYPE = 'USER_TYPE'
QUESTION_AUTHENTICATE = 'AUTHENTICATE'
QUESTION_NOTHING = 'NOTHING'
QUESTION_CHANGE_STATUS = 'CHANGE_STATUS'
QUESTION_EVENT_TYPE = 'EVENT_TYPES'

#NLP STUFF
import os.path
import sys
import json
from bot_services.jsonToFunc import sonToFunc

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

# CLIENT_ACCESS_TOKEN = '8839e93fbba447f0a8b93e6979aefce0'
# CLIENT_ACCESS_TOKEN = '549acac7e0384260ab147a73357ef602' ##thomas's API.ai agent
CLIENT_ACCESS_TOKEN = 'a0416a28f1bf43f0872f65ad1c159834' ##clara's API.ai agent
#NLP STUFF


class AnswerService:
    #TODO:make it more elegant if possible
    def getUsertype(answer):
        searchObj = re.search(r'\b[Ss]tudent\b',answer)
        if searchObj:
            return 'student'
        else:
            searchObj = re.search(r'\b[Ii]nstructor\b',answer)
            if searchObj:
                return 'instructor'
            else:
                return None

    # business logic
    def process_message(message):
        # Get user.
        user_id = (message['sender']['id'])
        user_info = CommunicationService.get_user_info(user_id).json()
        fbuser = UserService.getUser(user_id)

        # If user does not exist, create user, create conversation, and ask for user type first.
        if(fbuser is None):
            fbuser = UserService.create_new_user(user_info,user_id)
            conversation = UserService.create_new_conversation(fbuser)
            return "Hi, " + fbuser.first_name + "! " + MSG_ASK_FOR_USER_TYPE

        # If user exist, so must conversation. Get conversation.
        conversation = UserService.get_conversation(fbuser)
        msg = message['message']['text']

        # If the question is user type, check if the user answers with user type
        if(conversation.question == Question.get_question_type(QUESTION_USER_TYPE)):
            fbuser_type = AnswerService.getUsertype(msg)
            # User did not answer with his user type.
            if (fbuser_type is None):
                return MSG_ASK_FOR_USER_TYPE
            else:
                # Record user type.
                fbuser.set_user_type(fbuser_type)
                conversation.set_conversation_question(Question.get_question_type(QUESTION_NOTHING))
                return "Okay, you are a "+ fbuser_type + ". You can now authenticate anytime by typing [authenticate]."

        # if the question is changing the user type. verify the user enter a different type
        elif(conversation.question == Question.get_question_type(QUESTION_CHANGE_STATUS)):
            current_type = fbuser.user_type
            fbuser_type = AnswerService.getUsertype(msg)
            if(fbuser_type is None):
                conversation.set_conversation_question(Question.get_question_type(QUESTION_NOTHING))
                return "Sorry, the user type " + msg " does not exist"
            elif(fbuser_type != current_type):
                fbuser.set_user_type(fbuser_type)
                conversation.set_conversation_question(Question.get_question_type(QUESTION_NOTHING))
                return "Your new status is: " + fbuser_type + "."
            else:
                return "You already are " + fbuser_type + ", no changes were made."

        # If the question type is authentication, check the user's authentication status to do corresponding works.
        elif(conversation.question == Question.get_question_type(QUESTION_AUTHENTICATE)):
            reply = AuthenticationService.authenticationProcess(fbuser, msg)
            if(fbuser.authentication_status == AuthenticationService.AUTHENTICATION_NO):
                conversation.set_conversation_question(Question.get_question_type(QUESTION_NOTHING))
            if(fbuser.authentication_status == AuthenticationService.AUTHENTICATION_DONE):
                conversation.set_conversation_question(Question.get_question_type(QUESTION_NOTHING))
            return reply

        # If it's about event type
        elif(conversation.question == Question.get_question_type(QUESTION_EVENT_TYPE)):
            conversation.set_conversation_question(Question.get_question_type(QUESTION_NOTHING))
            if ('n/a' in msg):
                return "no type added"
            event = EventService.get_most_recent_event(conversation)
            try:
                event_types = EventService.parse_event_types(msg)
            except Exception as e:
                return str(e)
            EventService.add_types_to_event(event_types, event)
            return "the types are added to the event"

        # If the question is empty, the msg must be a question.
        elif(conversation.question == Question.get_question_type(QUESTION_NOTHING)):
            # API.AI STUFF
            ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
            request = ai.text_request()
            request.lang = 'de'  # optional, default value equal 'en'
            request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
            request.query = msg
            response = request.getresponse()
            apiJSON = response.read()
            str_apiJSON = apiJSON.decode('utf-8')
            jsonDict = json.loads(str_apiJSON)

            ##let users login regardless of their auth status
            if "action" in jsonDict["result"]:
                if jsonDict["result"]["action"] == "login":
                    return sonToFunc(jsonDict["result"], message)
            ##stops users that are not logged ie their auth is not done, from accessing the features in jsonFunc
            if (fbuser.authentication_status != AuthenticationService.AUTHENTICATION_DONE):
                return "You are not logged in. Please type login"
            else:
                return sonToFunc(jsonDict["result"], message)
        return msg
