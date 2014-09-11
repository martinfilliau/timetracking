import sys
import os

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


def get_events_from_ics(file):
    """Get events from an ics file
    """
    g = open(file,'r')
    cal = Calendar.from_ical(g.read())
    projects = {}
    for e in cal.walk('vevent'):
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


def main():
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('directory', action='store', help='Directory containing ics files')

    ns = parser.parse_args()
    
    files = get_ics_files(ns.directory)

    for file in files:
        sys.stdout.write("= {activity} =\n".format(activity=file.split('.ics')[0]))
        projects = get_events_from_ics(ns.directory+"/"+file)
        for name, length in projects.iteritems():
            sys.stdout.write("{name}: {length}\n".format(name=name, length=format_timedelta(length['total'])))


if __name__ == '__main__':
    main()