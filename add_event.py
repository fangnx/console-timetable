from functools import reduce
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json


SCOPES = 'https://www.googleapis.com/auth/calendar'
TIMEZONE = "Canada/Eastern"


def add_event():

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    course_name = input("Enter the course code (e.g., AAAA 100): ")
    activity_type = input("Type of events (e.g., Lecture, Tutorial, Lab): ")
    day_in_the_week = input("Day: ")
    location = input("Location: ")
    start_time = input("From what time (HH:MM:SS) does the " + activity_type + " start: ")
    end_time = input("At what time (HH:MM:SS) does the " + activity_type + " end: ")
    start_date = input("From what date (YYYY-MM-DD) does the " + activity_type + " start: ")
    end_date = input("On what date (YYYY-MM-DD) does the " + activity_type + " end: ")
    recurrence = True

    activity_data = {}
    activity_data["summary"] = course_name + ' ' + activity_type
    activity_data["location"] = location
    activity_data["start"] = {"dateTime": start_date + "T" + start_time,
                           "timeZone": TIMEZONE}
    activity_data["end"] = {"dateTime": start_date + "T" + end_time,
                         "timeZone": TIMEZONE}
    activity_data["recurrence"] = ["RRULE:FREQ=WEEKLY;UNTIL=" +
                                 reduce(lambda a,b: a+b, end_date.split("-"), "")]

    service.events().insert(calendarId='primary', body=activity_data).execute()
    print('Creation of event ' + course_name + ' ' + activity_type + " successful!")


    with open("courses_info.json", "r") as json_file:
        json_data = json.load(json_file)
        activities = json_data.get(course_name)["activities"]
        attributes = {'location', 'start', 'end', 'recurrence'}
        new_activities_data = {activity_type: {key: activity_data[key] for key in attributes}}
        json_data.get(course_name)["activities"].update(new_activities_data)

    with open("courses_info.json", "w") as json_file:
        json.dump(json_data, json_file)


if __name__ == '__main__':
    add_event()
