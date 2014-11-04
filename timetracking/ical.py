import os

from icalendar import Calendar

from timetracking.datetime_helpers import calculate_time, within


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