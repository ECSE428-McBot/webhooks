from pprint import pprint
from fb_mcbot.models import FBUser, Conversation, StudentSociety, Admin, Major, Course


class Question:
    question_type = {'NOTHING': 0, 'USER_TYPE': 1, 'AUTHENTICATE': 2, 'EVENT_NAME': 3,
                     'EVENT_LOCATION': 4, 'EVENT_DESCRIPTION': 5, 'EVENT_LINK': 6, 'EVENT_DATE': 7,
                     'EVENT_CONFIRMATION': 8, 'CHANGE_STATUS': 9}

    def get_question_type(question):
        try:
            result = Question.question_type.get(question)
        except KeyError:
            pprint("Internal Error! " + question + " is not a question type!")
        return result

class UserService:
    def getUser(userid):
        try:
            user = FBUser.objects.get(user_id=userid)
        except FBUser.DoesNotExist:
            pprint("User id not found in db, the user does not exist.")
            return None
        return user

    def getAllUsers():
        try:
            users = FBUser.objects.all()
        except FBUser.DoesNotExist:
            pprint("DataBase Error")
            return None
        return users

    def getStudentsInCourse(courseName):
        try:
            course = Course.objects.get(name=courseName)
        except Course.DoesNotExist:
            raise
        return course.fbuser_set.all()

    def create_new_user(user_info,user_id):
        pprint("Creating new user")
        firstname = user_info['first_name']
        lastname = user_info['last_name']
        timezone = user_info['timezone']
        new_user = FBUser(first_name=firstname, last_name=lastname, user_id=user_id, timezone=timezone)
        new_user.save()
        return new_user

    def create_new_conversation(fbuser):
        pprint("Creating new conversation")
        new_conversation = Conversation()
        new_conversation.fbuser = fbuser
        # default question USER_TYPE
        new_conversation.question = Question.get_question_type('USER_TYPE')
        new_conversation.save()
        return new_conversation

    def get_conversation(fbuser):
        try:
            conversation = Conversation.objects.get(fbuser=fbuser)
        except Conversation.DoesNotExist:
            pprint("Conversation with " + fbuser.user_id + " not found in db")
            return None
        return conversation

    def get_student_society(fbuser):
        try:
            ssociety = StudentSociety.objects.get(fbuser=fbuser)
        except StudentSociety.DoesNotExist:
            pprint("Student StudentSociety with " + fbuser.user_id + " not found in db")
            return None
        return ssociety

    def is_admin(fbuser):
        try:
            Admin.objects.get(fbuser=fbuser)
            return True
        except Admin.DoesNotExist:
            return False

    def get_major(fbuser):
        print (fbuser)
        major = fbuser.major;
        if(major):
            return True
        else:
            return False

    def set_major(fbuser,major):
        fbuser.major = Major.objects.get(name=major)
        fbuser.save()
        return ("You've set your major to " + fbuser.major.name + ". What courses are you taking?")

    def add_courses(fbuser,courses):
        for course in courses:
            c = Course.objects.get(pk=course)
            fbuser.courses.add(c)
        fbuser.save()
        response = ""
        newCourses = fbuser.courses.all()
        for course in newCourses:
            response += (course.name + " ,")
        return ("Your courses are now: " + response)
