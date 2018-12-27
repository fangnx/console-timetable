import sys
from functools import reduce
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

import argparse
parser = argparse.ArgumentParser()

SCOPES = 'https://www.googleapis.com/auth/calendar'


test_event = {
  'summary': 'Appointment',
  'location': 'Somewhere',
  'start': {
    'dateTime': '2019-01-03T10:00:00',
    'timeZone': 'America/Los_Angeles'
  },
  'end': {
    'dateTime': '2019-01-03T10:25:00',
    'timeZone': 'America/Los_Angeles'
  },
  'recurrence': [
    'RRULE:FREQ=WEEKLY;UNTIL=20190127',
  ]
}





DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
TIMEZONE = "Canada/Eastern"

def format_time(str):

    return 0


def add_event_manually():

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    event_name = input("Enter the name of the event: ")
    day_in_the_week = input("Day: ")
    start_time = input("From what time (HH:MM:SS) does the event start: ")
    end_time = input("At what time (HH:MM:SS) does the event end: ")
    start_date = input("From what date (YYYY-MM-DD) does the event start: ")
    end_date = input("On what date (YYYY-MM-DD) does the event end: ")
    recurrence = True

    event_info = {}
    event_info["summary"] = event_name
    event_info["start"] = {"dateTime": start_date + "T" + start_time,
                           "timeZone": TIMEZONE}
    event_info["end"] = {"dateTime": start_date + "T" + end_time,
                         "timeZone": TIMEZONE}
    event_info["recurrence"] = ["RRULE:FREQ=WEEKLY;UNTIL=" +
                                 reduce(lambda a,b: a+b, end_date.split("-"), "")]

    print(event_info)
    service.events().insert(calendarId='primary', body=event_info).execute()





def out_console():

    header = ""
    for d in DAYS:
        header += ("|---" + d + "---|")

    print(header)


    with open("t.json", "r") as data:
        print(json.load(data))


if __name__ == '__main__':
    add_event_manually()
    # gcalendar()