"""Print our structures to stdout
"""

import sys
import csv

from timetracking.formatters import format_timedelta


def write(activities):
    """Write activities to stdout
    :param activities: dict structure
    """
    csv_writer = csv.writer(sys.stdout)
    csv_writer.writerow(['Activity', 'Project', 'Time spent'])
    for activity in activities:
        projects = activities[activity]
        for name, length in projects.iteritems():
            total_project = length['total']
            td_string = format_timedelta(total_project)
            csv_writer.writerow([activity, name, td_string])
