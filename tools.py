from datetime import datetime


def get_weekday_index(time):

    year, month, day = time.split('T')[0].split('-')
    weekday_index = datetime(int(year), int(month), int(day)).weekday()
    return weekday_index


def index_to_weekday(index):

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return weekdays[index]


