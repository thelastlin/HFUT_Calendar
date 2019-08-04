#!/usr/bin/env python3
import requests
import json
import hfut_calendar_tools
import sys


def main(argv):
    userinfo = {
        "password": argv[2],
        "username": argv[1]
    }
    login_session = hfut_calendar_tools.get_login_sessions(userinfo)

    student_id = login_session.get('http://jxglstu.hfut.edu.cn/eams5-student/for-std/course-table').url.split('/')[-1]

    get_data_payload = {
        'bizTypeId': 23,
        'semesterId': 74,
        'dataId': student_id
    }
    get_data_req = login_session.get(hfut_calendar_tools.URL.get_data, params=get_data_payload)
    get_data_req.raise_for_status()
    get_data_json = json.loads(get_data_req.text)
    classId = get_data_json["lessonIds"]
    classStatus = get_data_json["courseId2CourseTextbookStat"]
    dataum_post_json = {
        "lessonIds": classId,
        "weekIndex": "",
        "studentId": student_id
    }
    dataum_req = requests.post(hfut_calendar_tools.URL.dataum, cookies=login_session.cookies, json=dataum_post_json)
    dataum_json = json.loads(dataum_req.text)["result"]
    class_dict = hfut_calendar_tools.gen_class_dict(dataum_json["lessonList"])

    schedule_list = dataum_json["scheduleList"]

    calendar = hfut_calendar_tools.gen_calendar(class_dict, schedule_list)
    ical_file = open("calendar.ics", "wb")
    ical_file.write(calendar.to_ical())
    ical_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] == "help":
        print("Usage: ./generate_ics.py username password")
        exit(-1)
    main(sys.argv)

