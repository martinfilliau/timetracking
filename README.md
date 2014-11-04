# timetracking

[![Build Status](https://travis-ci.org/martinfilliau/timetracking.svg?branch=master)](https://travis-ci.org/martinfilliau/timetracking)

Track time from ics files

An ics file is identified as an activity (e.g. SysAdmin, Development, Meeting), events are aggregated based on their names.

## Example

The following command will analyse all the files ending with `.ics` in the `tt` directory:

    python tt.py /home/martin/tt

It will produce the following output, assuming that we have calendars `SysAdmin.ics`, `Admin.ics`, `Development.ics`:

    = Admin =
    timesheeting update: 0 h 15 m
    move desk: 0 h 15 m
    hr: 23 h 45 m
    talks.ox: 7 h
    maps.ox: 6 h 35 m
    [...]
    > TOTAL: 48 h 10 m
    = Development =
    maps.ox: 53 h 50 m
    [...]
    > TOTAL: 216 h 30 m
    = SysAdmin =
    maps.ox: 13 h
    talks.ox: 0 h 30 m
    [...]
    > TOTAL: 23 h 45 m

You can specify a start and end date to filter the calendars, for example:

    python tt.py /home/martin/calendars 01/10/2014 31/10/2014

`--output` lets you select if the output should be CSV or TXT

    python tt.py /home/martin/calendars 01/10/2014 31/10/2014 --output CSV
