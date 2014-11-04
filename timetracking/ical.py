"""Handle iCalendars to our structure
"""

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
            if not within(event['DTSTART'].dt, from_date, to_date):
                continue
        name = str(event['SUMMARY']).lower()
        if '-' in name:
            project_name = name.split('-')[0].strip()
        else:
            project_name = name
        event_start = event['DTSTART'].dt
        event_end = event['DTEND'].dt
        project_total = calculate_time(event_start, event_end)
        if project_name in projects:
            new_total = projects[project_name]['total'] + project_total
            projects[project_name]['total'] = new_total
        else:
            projects[project_name] = {}
            projects[project_name]['total'] = project_total
    return projects
