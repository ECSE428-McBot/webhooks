import json
import _datetime
import pytz
import re
from bot_services.user_service import UserService, Question
from bot_services.communication_service import CommunicationService
from datetime import datetime
from dateutil.parser import parse
from fb_mcbot.models import Event, EventType

QUESTION_EVENT_NAME = 'EVENT_NAME'
QUESTION_EVENT_LOCATION = 'EVENT_LOCATION'
QUESTION_EVENT_DESCRIPTION = 'EVENT_DESCRIPTION'
QUESTION_EVENT_LINK = 'EVENT_LINK'
QUESTION_EVENT_DATE = 'EVENT_DATE'
QUESTION_EVENT_CONFIRMATION = 'EVENT_CONFIRMATION'
QUESTION_NOTHING = 'NOTHING'

class EventService:

    def get_event_id_from_link(link):
        print(link)
        p = re.compile('\d+(?!=\d)')
        m = p.search(link)
        if not m:
            raise Exception(link + 'is not a valid link')
        return m.group(0)

    def parse_event_types(msg):
        event_types = msg.split(' ')
        for t in event_types:
            try:
                EventType.objects.get(name=t)
            except EventType.DoesNotExist:
                raise Exception('\'' + t + '\'' + ' is not a valid event type')
        return event_types

    def get_event_from_link(link):
        try:
            eventId = EventService.get_event_id_from_link(link)
        except Exception as e:
            raise
        try:
            event = Event.objects.get(id=eventId)
        except Event.DoesNotExist:
            raise Exception('event does not exist')
        return event

    def create_new_event(conversation, link):
        ssociety = UserService.get_student_society(conversation.fbuser)
        eventId = EventService.get_event_id_from_link(link)
        if (eventId is None):
            raise
        try:
            event = CommunicationService.get_event_info(eventId)
        except Exception:
            raise
        event_info = event.json()
        new_event = Event()
        new_event.link = link
        new_event.creator = ssociety
        new_event.name = event_info['name']
        new_event.id = eventId
        new_event.event_time = parse(event_info['end_time']).strftime('%Y-%m-%d %H:%M:%S')
        new_event.category = event_info['category']
        new_event.save()

    def add_types_to_event(event_types, event):
        for t in event_types:
            event.types.add(EventType.objects.get(name=t))

    def get_most_recent_event(conversation):
        ssociety = UserService.get_student_society(conversation.fbuser)
        # recent_event = Event.objects.filter(creator = ssociety).order_by('creation_time')[0]
        recent_event = Event.objects.filter(creator = ssociety).latest('creation_time')
        return recent_event

    def search_event_by_type(type_name):
        try:
            event_type = EventType.objects.get(name=type_name)
        except EventType.DoesNotExist:
            raise Exception(type_name + ' is not a valid event type')
        return event_type.event_set.all()

    def initEvent(conversation, link):
        try:
            EventService.create_new_event(conversation, link)
            return "Event created, please add some types to the event, for example 'sale food'. type 'n/a' to skip"
        except Exception as e:
            return "Error occured while creating the event. Event might already exists"

    def get_events():
        now = datetime.now()
        events =  Event.objects.filter(event_time__gte = now)
        result = ""
        for e in events:
            result += "\n[" + e.name + "]: " + e.link
        return result
