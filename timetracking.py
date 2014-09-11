import sys
import os
from datetime import datetime

from pytz import timezone
from icalendar import Calendar


def get_ics_files(directory):
    """Get all filenames ending with .ics from a directory
    """
    ics = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.ics'):
                ics.append(filename)
        break
    return ics


def get_events_from_ics(file, from_date, to_date):
    """Get events from an ics file
    """
    g = open(file,'r')
    cal = Calendar.from_ical(g.read())
    projects = {}
    for e in cal.walk('vevent'):
        if from_date and to_date:
            if not within(e, from_date, to_date):
                continue
        name = str(e['SUMMARY']).lower()
        if '-' in name:
            project_name = name.split('-')[0].strip()
            task_name = name.split('-')[1].strip()
        else:
            project_name = name
            task_name = None
        if project_name in projects:
            projects[project_name]['total'] = projects[project_name]['total'] + calculate_time(e)
        else:
            projects[project_name] = {}
            projects[project_name]['total'] = calculate_time(e)
    return projects


def calculate_time(event):
    """Get timedelta from event, based on start/end date
    """
    start = event['DTSTART'].dt
    end = event['DTEND'].dt
    return end - start

def within(event, from_date, to_date):
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
        return "{hours} h {minutes} m".format(hours=int(hours), minutes=int(minutes))


def mkdate(datestr):
    """Date from string (input)
    """
    return datetime.strptime(datestr, '%d/%m/%Y')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('directory', action='store', help='Directory containing ics files')
    parser.add_argument('from_date', type=mkdate, help='Date to start', nargs='?', default=None)
    parser.add_argument('to_date', type=mkdate, help='Date to end', nargs='?', default=None)
    parser.add_argument('--timezone', action='store', dest='timezone', help='Timezone', default='Europe/London')

    ns = parser.parse_args()
    
    if ns.from_date and ns.to_date:
        t = timezone(ns.timezone)
        from_date = t.localize(ns.from_date)
        to_date = t.localize(ns.to_date)
    else:
        from_date = None
        to_date = None

    files = get_ics_files(ns.directory)

    for file in files:
        sys.stdout.write("= {activity} =\n".format(activity=file.split('.ics')[0]))
        projects = get_events_from_ics(ns.directory+"/"+file, from_date, to_date)
        for name, length in projects.iteritems():
            sys.stdout.write("{name}: {length}\n".format(name=name, length=format_timedelta(length['total'])))


if __name__ == '__main__':
    main()