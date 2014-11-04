"""Functions to analyse events from calendars in iCalendar format
"""

from pytz import timezone

from timetracking.formatters import date_from_string
from timetracking.ical import get_ics_files, get_events_from_ics
from timetracking.writers.stdout import write as txt_write
from timetracking.writers.csv_output import write as csv_write

OUTPUT = {
    'TXT': txt_write,
    'CSV': csv_write
}


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
    parser.add_argument('--output',
                        action='store',
                        dest='output',
                        default='TXT',
                        help="Output: {available_functions})".format(
                            available_functions=', '.join(OUTPUT.iterkeys())))

    args = parser.parse_args()

    if args.from_date and args.to_date:
        timez = timezone(args.timezone)
        from_date = timez.localize(args.from_date)
        to_date = timez.localize(args.to_date)
    else:
        from_date = None
        to_date = None

    ics_files = get_ics_files(args.directory)
    activities = {}
    for ics_file in ics_files:
        projects = get_events_from_ics(args.directory+"/"+ics_file,
                                       from_date, to_date)
        activities[ics_file.split('.ics')[0]] = projects

    writer = OUTPUT.get(args.output)
    writer(activities)


if __name__ == '__main__':
    main()
