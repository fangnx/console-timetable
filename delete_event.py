import sys
from functools import reduce
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

import argparse
parser = argparse.ArgumentParser()

SCOPES = 'https://www.googleapis.com/auth/calendar'

def delete_event_manually():

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    current_time = datetime.now().isoformat() + 'Z'
    max_time = (datetime.now() + timedelta(days = 365*2)).isoformat() + 'Z'
    raw_events = service.events().list(
        calendarId = 'primary', timeMin = current_time, singleEvents = True,
        orderBy = 'startTime', timeMax = max_time).execute()

    events = [{'summary': i.get('summary'), 'id': i.get('id'),'startTime': i.get('start').get('dateTime'),
               'endTime': i.get('end').get('dateTime')} for i in (raw_events.get('items'))]

    print(events)
    event_name = input("Enter the name of the event you want to delete: ")
    is_deleted = False
    for event in events:
        if event.get('summary') == event_name:
            service.events().delete(calendarId = 'primary', eventId = event.get('id')).execute()
            is_deleted = True

    print('Deletion of event ' + event_name + "successful!") if is_deleted else print('Event not found.')


if __name__ == '__main__':
    delete_event_manually()

