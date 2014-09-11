import sys
import os

from icalendar import Calendar


def get_ics_files(directory):
    """Get all files ending with .ics from a directory
    """
    ics = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.ics'):
                ics.append(filename)
        break
    return ics


def get_events_from_ics(file):
    g = open(file,'r')
    cal = Calendar.from_ical(g.read())
    projects = {}
    for e in cal.walk('vevent'):
        name = str(e['SUMMARY']).lower()
        if name in projects:
            projects[name] = projects[name] + calculate_time(e)
        else:
            projects[name] = calculate_time(e)
    return projects


def calculate_time(event):
    start = event['DTSTART'].dt
    end = event['DTEND'].dt
    return end - start


def main():
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('directory', action='store', help='Directory containing ics files')

    ns = parser.parse_args()
    
    files = get_ics_files(ns.directory)

    sys.stderr.write("==> Found {count} ics files\n".format(count=len(files)))

    for file in files:
        sys.stdout.write("= {activity} =\n".format(activity=file.split('.ics')[0]))
        projects = get_events_from_ics(ns.directory+"/"+file)
        for name, length in projects.iteritems():
            sys.stdout.write("{name}: {length} h\n".format(name=name, length=length.seconds//3600))

    #sys.stdout.write(geojson_dumps(collection))


if __name__ == '__main__':
    main()