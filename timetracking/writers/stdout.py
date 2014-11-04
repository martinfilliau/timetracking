"""Print our structures to stdout
"""

import sys
from datetime import timedelta

from timetracking.formatters import format_timedelta


def write(activities):
    """Write activities to stdout
    :param activities: dict structure
    """
    for activity in activities:
        total_time_activity = timedelta()
        sys.stdout.write("= {activity} =\n".format(
            activity=activity))
        projects = activities[activity]
        for name, length in projects.iteritems():
            total_project = length['total']
            total_time_activity += total_project
            td_string = format_timedelta(total_project)
            sys.stdout.write("{name}: {length}\n".format(name=name,
                                                         length=td_string))
        sys.stdout.write("> TOTAL: {length}\n".format(
            length=format_timedelta(total_time_activity)))
