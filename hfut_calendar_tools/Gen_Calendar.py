from typing import List, Any

from icalendar import Calendar, Event
from uuid import uuid1
import datetime


def gen_calendar(class_dict: dict, schedule_list: list) -> Calendar:
    calendar = Calendar()
    calendar['version'] = '2.0'
    calendar['prodid'] = '-//HFUT//xCalendar//CN'
    merged_schedule_list: List[dict] = []
    for lesson in schedule_list:
        if (not merged_schedule_list) or (not(lesson["lessonId"] == merged_schedule_list[-1]["lessonId"] and lesson["date"] == merged_schedule_list[-1]["date"] and lesson[
                'startTime'] == merged_schedule_list[-1]["startTime"])):
            merged_schedule_list.append(lesson)
        else:
            merged_schedule_list[-1].update(personName=merged_schedule_list[-1]["personName"]+' ' + lesson["personName"])
    for lesson in merged_schedule_list:
        event = Event()
        event.add("summary", class_dict[lesson["lessonId"]])
        event.add("description", lesson["personName"])
        event.add("location", (lesson["room"] is None) and " " or lesson["room"]["nameZh"])
        schedule_time_of_start = '{0} {1}:{2}:00'.format(lesson["date"], lesson['startTime'] // 100,
                                                         lesson['startTime'] % 100)
        schedule_time_of_end = '{0} {1}:{2}:00'.format(lesson["date"], lesson['endTime'] // 100,
                                                       lesson['endTime'] % 100)
        dtstart = datetime.datetime.strptime(schedule_time_of_start, "%Y-%m-%d %H:%M:%S")
        dtend = datetime.datetime.strptime(schedule_time_of_end, "%Y-%m-%d %H:%M:%S")
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)
        event.add('uid', str(uuid1()) + '@HFUT')
        event.add("dtstamp", datetime.datetime.now())
        calendar.add_component(event)
    return calendar
