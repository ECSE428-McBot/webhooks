# test json input
inTest0 = {
    "action": "walksafe",
    "location": "Lunch with Mary Johnson"
}
inTest1 = {
    "action": "walksafe",
    "location": "Lunch with Mary Johnson",
    "number": "123"
}
inTest2 = {

}
inTest3 = {
    "location": "Lunch with Mary Johnson"
}
inTest4 = {
    "action": "commands",
    "location": "Lunch with Mary Johnson"
}


# import classes for functions here
from bot_services.calendar_service import CalendarService
from bot_services.user_service import UserService, Question
from bot_services.authentication_service import AuthenticationService
from bot_services.event_service import EventService
from bot_services.mcgill_event_service import McgillEventService
from bot_services.communication_service import CommunicationService

QUESTION_CHANGE_STATUS = 'CHANGE_STATUS'
QUESTION_USER_TYPE = 'USER_TYPE'
QUESTION_AUTHENTICATE = 'AUTHENTICATE'
QUESTION_NOTHING = 'NOTHING'
QUESTION_EVENT_TYPE = 'EVENT_TYPES'
QUESTION_ADD_LINK = 'ADD_EVENT_TYPE'

def sonToFunc(inSon, message):
    if inSon == {}:
        return "Null input"
    if "action" in inSon.keys():
        apiAction = inSon["action"]
        if "parameters" in inSon.keys():
            parameters = inSon["parameters"]
    else:
        return "Invalid input"

    # If user enters "login", check if he/she has already been authenticated to do corresponding works.
    if apiAction == "login":
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        conversation = UserService.get_conversation(fbuser)
        msg = message['message']['text']
        if (fbuser.authentication_status == AuthenticationService.AUTHENTICATION_DONE):
            return "You have already finished Authentication."
        else:
            conversation.set_conversation_question(Question.get_question_type(QUESTION_AUTHENTICATE))
        return AuthenticationService.authenticationProcess(fbuser, msg)
        # return "login"
        # return login()

    elif apiAction == "logout":
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        conversation = UserService.get_conversation(fbuser)
        AuthenticationService.resetAuthentication(fbuser)
        conversation.set_conversation_question(Question.get_question_type(QUESTION_NOTHING))
        return "Your are logged out."
        # return "logout"
        # return logout()

    elif apiAction == "rsvp":
        # if "event" in inSon.keys() and "status" in inSon.keys():
        #     return ["rsvp", inSon["event"], inSon["status"]]
        #     # return rsvp(inSon["event"],inSon["status"])
        # else:
        #     return "Error: Incomplete Input"
        return EventService.get_events()

    elif apiAction == "addEntryCalendar":
        if "name" in parameters.keys() and "date" in parameters.keys() and "time" in parameters.keys() and "description" in parameters.keys():
            name = parameters["name"]
            description = parameters["description"]
            date = parameters["date"]
            time = parameters["time"]
            return CalendarService().create_event_client(name,description)
            # return calenderSet(inSon["event"],inSon["date"],inSon["time"])
        else:
            return "Error: Incomplete Input"

    elif apiAction == "linkEvent":
        if "event" not in parameters.keys():
            return "What's the name of the event?"
        if "url" not in parameters.keys():
            return "What's the link of the event?"
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        conversation = UserService.get_conversation(fbuser)
        ssociety = UserService.get_student_society(fbuser)
        if (ssociety is None):
            return "Sorry you can't post event because you are not student society"
        reply = EventService.initEvent(conversation, parameters['url'])
        conversation.set_conversation_question(Question.get_question_type(QUESTION_EVENT_TYPE))
        return reply

    elif apiAction == "add_event_type":
        if "url" not in parameters.keys():
            return "what's the event?"
        if "type" not in parameters.keys():
            return "I cannot resolve the types"
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        conversation = UserService.get_conversation(fbuser)
        ssociety = UserService.get_student_society(fbuser)
        if (ssociety is None):
            return "Sorry you can't do that because you are not student society"
        #get event
        try:
            event = EventService.get_event_from_link(parameters['url'])
        except Exception as e:
            return str(e)
        #parse types
        try:
            event_types = EventService.parse_event_types(parameters['type'])
        except Exception as e:
            return str(e)
        EventService.add_types_to_event(event_types, event)
        return "the types are added to the event"
    
    elif apiAction == "search_event":
        if 'type' in parameters.keys():
            events = EventService.search_event_by_type(parameters['type'])
            return "Events of type " + parameters['type'] + ": " + [event.link for event in events].join(", ")

    # If user enters "change" we start the "change my user type" conversation
    elif apiAction == "changeStatus":
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        if "status" in parameters.keys() and (parameters['status'] == 'instructor' or parameters['status'] == 'student'):
            if (fbuser.user_type == parameters['status']):
                return "You already are: " +  fbuser.user_type + ", no changes were made."
            else :
                fbuser.user_type = parameters['status']
                fbuser.save()
                return "Your new status is: " + fbuser.user_type + "."
        else:
            conversation = UserService.get_conversation(fbuser)
            conversation.set_conversation_question(Question.get_question_type(QUESTION_CHANGE_STATUS))
        return "Please enter your new status."

    elif apiAction == "minerva":
        if "username" in inSon.keys() and "password" in inSon.keys():
            return ["connectMinerva", inSon["username"], inSon["password"]]
            # return connectMinerva(inSon["username"],inSon["password"])
        else:
            return "Error: Incomplete Input"

    elif apiAction == "connect":
        if "calender" in inSon.keys() and "url" in inSon.keys():
            return ["connectCalender", inSon["calender"], inSon["url"]]
            # return connectCalender(inSon["calender"],inSon["url"])
        else:
            return "Error: Incomplete Input"

    elif apiAction == "deadlines":
        return McgillEventService().listAllDeadlines()

    elif apiAction == "commands":
        return ["listCommands"]
        # return listCommands()

    elif apiAction == "mac":
        return ["macBus"]
        # return macBus()

    elif apiAction == "broadcast":
        if "class" not in parameters.keys():
            return "I can't resolve the class name"
        if "message" not in parameters.keys():
            return "I can't resolve the message you want to broadcast"
        #check if user is instructor
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        if not (fbuser.user_type == 'instructor'):
            return "Sorry, only instructors can broadcast message"
        try:
            students_in_class = UserService.getStudentsInCourse(parameters['class'])
        except:
            return "I'm unable to find student taking this class. I don't think this class exist"
        CommunicationService.post_facebook_message_to_class(students_in_class, parameters['message'])
        return "your message is successfully broadcasted to the class " + parameters['class']

    elif apiAction == "msgAll":
        if "message" not in parameters.keys():
            return "what's the message?"
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        if(UserService.is_admin(fbuser)):
            CommunicationService.post_facebook_message_to_all(parameters['message'])
            return"Your message has been sent to all registered users"
        else:
            return "Only admins can message all users"

    elif apiAction == "share":
        if "event" in inSon.keys():
            return ["shareEvent", inSon["event"]]
            # return shareEvent(inSon["event"])
        else:
            return "Error: Incomplete Input"

    elif apiAction == "delete":
        if "event" in inSon.keys():
            return ["deleteEvent", inSon["event"]]
            # return deleteEvent(inSon["event"])
        else:
            return "Error: Incomplete Input"

    elif apiAction == "status":
        if "event" in inSon.keys():
            return ["statusEvent", inSon["event"]]
            # return statusEvent(inSon["event"])
        else:
            return "Error: Incomplete Input"

    elif apiAction == "link":
        if "event" in inSon.keys() and "page" in inSon.keys():
            return ["linkEvent", inSon["event"], inSon["page"]]
            # return linkEvent(inSon["event"],inSon["page"])
        else:
            return "Error: Incomplete Input"

    elif apiAction == "my":
        return ["curStatus"]
        # return curStatus()

    elif apiAction == "sayingHello":
        return "Hi! How may I help you?"

    elif apiAction == "askEventsMajor":
        ## return either a response of upcoming events in their major or ask them to input their major/courses
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        if (UserService.get_major(fbuser)):
            print (fbuser.major)
            return McgillEventService().get_event_in_major(fbuser.major)
            return "Querying for course events"
        else:
            ## ask for major
            return "I don't know what you major in, could you tell me?"

    elif apiAction == "addMajor":
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        if "major" in parameters.keys():
            if(parameters['major'] == ""):
                return "I didn't get what you major in.. try again?"
            else:
                return (UserService.set_major(fbuser, parameters['major']))

    elif apiAction == "addCourses":
        user_id = (message['sender']['id'])
        fbuser = UserService.getUser(user_id)
        if "courses" in parameters.keys():
            if not parameters['courses']:
                return "I didn't get what courses you're taking.. try again?"
            else:
                return (UserService.add_courses(fbuser, parameters['courses']))
    else:
        return "Invalid input"


# print (sonToFunc(inTest0))
# print (sonToFunc(inTest1))
# print (sonToFunc(inTest2))
# print (sonToFunc(inTest3))
# print (sonToFunc(inTest4))
