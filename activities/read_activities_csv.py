import csv
import json
import datetime
import dateutil.tz
import dateutil.parser
from dateutil import zoneinfo

DAWN_TIME = datetime.datetime(1970, 1, 1, tzinfo=dateutil.tz.tzutc())

# Developer Note: ONLY 3 Activities Supported
# TODO: add more from here: https://developers.google.com/fit/rest/v1/reference/activity-types
activitity_types = {
'Walking': 7,
'Running': 8,
'Elliptical': 25
}

def nano(val):
  """Converts a number to nano (str)."""
  return '%d' % (int(val) * 1e9)

def epoch_of_time_str(dateTimeStr, tzinfo):
  log_time = dateutil.parser.parse(dateTimeStr).replace(tzinfo=tzinfo)
  return (log_time - DAWN_TIME).total_seconds()

def read_activities_csv():
    print "Reading Activities ..."
    is_header = True
    activities = []
    with open('activities.csv', 'rb') as csvfile:
        activities_reader = csv.reader(csvfile, delimiter=',')
        for row in activities_reader:
            if is_header:
                is_header=False
                continue
            data = json.loads(row[6])
            activities.append(dict(
                start_time=epoch_of_time_str(row[0], zoneinfo.gettz(row[4])),
                end_time=epoch_of_time_str(row[1], zoneinfo.gettz(row[4])),
                activity_type=activitity_types.get(row[5]),
                calories=data['calories'],
                distance=data['distance'],
                steps=data['steps']
                ))
    return activities

def read_activities_csv_with_gfit_format():
    activities = read_activities_csv()
    gfit_activities = []
    for activity in activities:
        gfit_activities.append(dict(
            dataTypeName='com.google.activity.segment',
            startTimeNanos=nano(activity["start_time"]),
            endTimeNanos=nano(activity["end_time"]),
            value=[dict(intVal=activity["activity_type"])],
        ))
    return gfit_activities

if __name__=="__main__":
    gfit_activities = read_activities_csv_with_gfit_format()
