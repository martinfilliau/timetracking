# timetracking

[![Build Status](https://travis-ci.org/martinfilliau/timetracking.svg?branch=master)](https://travis-ci.org/martinfilliau/timetracking)

Get some statistics from iCalendar files.

This is mainly used to track time spent doing different activities (such as "SysAdmin", "Development"...) on
various projects, useful to aggregate values for timesheet purpose.

## Model

An **iCalendar file** is identified as an **activity** (e.g. "SysAdmin", "Development"...).

Each **calendar event** should be named as follow: "PROJECT NAME - description". Description is not mandatory but the
`PROJECT NAME` should follow a consistent pattern as it will be used to aggregate all the values per project.

It will be soon possible to select which dimension (i.e. "project" or "activity") should be the main
one used for aggregation (i.e. get totals per project or per activity).

| Type / Dimension         | Project first | Activity first |
|--------------------------|---------------|----------------|
| Header (from file)       | Project       | Activity       |
| Title (from iCal events) | Activity      | Project        |

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

The argument `--output` lets you select if the output should be CSV or TXT

    python tt.py /home/martin/calendars 01/10/2014 31/10/2014 --output CSV

## Roadmap

* Improve test coverage
* Add the ability to select the main dimension (i.e. `activity` or `project`, to sort by either of them)
* Allow configuration of the separator between "project - description" for calendars' events
