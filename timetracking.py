"""Functions to analyse events from calendars in iCalendar format
"""

import sys
import os
from datetime import datetime, timedelta

from pytz import timezone
from icalendar import Calendar


def get_ics_files(directory):
    """Get all filenames ending with .ics from a directory
    """
    ics = []
    for (_, _, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.ics'):
                ics.append(filename)
        break
    return ics


def get_events_from_ics(filepath, from_date, to_date):
    """Get events from an ics file
    """
    ics_file = open(filepath, 'r')
    cal = Calendar.from_ical(ics_file.read())
    projects = {}
    for event in cal.walk('vevent'):
        if from_date and to_date:
            if not within(event, from_date, to_date):
                continue
        name = str(event['SUMMARY']).lower()
        if '-' in name:
            project_name = name.split('-')[0].strip()
        else:
            project_name = name
        if project_name in projects:
            new_total = projects[project_name]['total'] + calculate_time(event)
            projects[project_name]['total'] = new_total
        else:
            projects[project_name] = {}
            projects[project_name]['total'] = calculate_time(event)
    return projects


def calculate_time(event):
    """Get timedelta from event, based on start/end date
    """
    start = event['DTSTART'].dt
    end = event['DTEND'].dt
    return end - start


def within(event, from_date, to_date):
    """Check if given vEvent is between two datetimes
    :param event: vEvent (iCal)
    :param from_date: date start
    :param to_date: date end
    :return True if vEvent is between the two dates else False
    """
    return from_date < event['DTSTART'].dt < to_date


def format_timedelta(delta):
    """Format a timedelta object for human reading
    (Only handles hours/minutes for now)
    """
    seconds = delta.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes = remainder // 60
    if minutes == 0:
        return "{hours} h".format(hours=int(hours))
    else:
        return "{hours} h {minutes} m".format(hours=int(hours),
                                              minutes=int(minutes))


def date_from_string(date_string):
    """Date from string (input)
    :param date_string: date as string
    :return datetime object
    """
    return datetime.strptime(date_string, '%d/%m/%Y')


def main():
    """Main method
    """
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('directory',
                        action='store',
                        help='Directory containing ics files')
    parser.add_argument('from_date',
                        type=date_from_string,
                        help='Date to start',
                        nargs='?',
                        default=None)
    parser.add_argument('to_date',
                        type=date_from_string,
                        help='Date to end',
                        nargs='?',
                        default=None)
    parser.add_argument('--timezone',
                        action='store',
                        dest='timezone',
                        help='Timezone',
                        default='Europe/London')

    args = parser.parse_args()

    if args.from_date and args.to_date:
        timez = timezone(args.timezone)
        from_date = timez.localize(args.from_date)
        to_date = timez.localize(args.to_date)
    else:
        from_date = None
        to_date = None

    ics_files = get_ics_files(args.directory)

    for ics_file in ics_files:
        total_time_activity = timedelta()
        sys.stdout.write("= {activity} =\n".format(
            activity=ics_file.split('.ics')[0]))
        projects = get_events_from_ics(args.directory+"/"+ics_file,
                                       from_date, to_date)
        for name, length in projects.iteritems():
            total_project = length['total']
            total_time_activity += total_project
            sys.stdout.write("{name}: {length}\n".format(name=name,
                                                         length=format_timedelta(total_project)))
        sys.stdout.write("> TOTAL: {length}\n".format(
            length=format_timedelta(total_time_activity)))


if __name__ == '__main__':
    main()
