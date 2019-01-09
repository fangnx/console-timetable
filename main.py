import os
import json
import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from tools import get_weekday_index, index_to_weekday

import argparse
parser = argparse.ArgumentParser()


def add_course():

    try:
        file = open("courses_info.json", "r")
        json_data = json.load(file)

    except FileNotFoundError:
        file = open("courses_info.json", "w+")
        json_data = {"user": "fnx"}
        file.write(str(json_data))

    course_name = input("Enter the course code: ")
    instructor = input("Enter the instructor name: ")
    activities = {}
    course_data = {
        course_name: {
            "instructor": instructor,
            "activities": activities
        }
    }

    json_data.update(course_data)
    with open("courses_info.json", 'w') as file:
        json.dump(json_data, file)


def show_all_courses():

    out = []
    with open("courses_info.json", "r") as file:
        json_data = json.load(file)

    for key in json_data:
        if re.compile(r"[a-zA-Z]{1,4}\s").match(key):
            out.append(key)

    print(out)


def console_out():

    header = ''
    for i in range(7):
        header += '|+++ ' + index_to_weekday(i) + ' +++|'

    print(header)


if __name__ == '__main__':
    add_course()
    show_all_courses()
