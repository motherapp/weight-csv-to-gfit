import csv
import datetime
import dateutil.tz
import dateutil.parser
from dateutil import zoneinfo

DAWN_TIME = datetime.datetime(1970, 1, 1, tzinfo=dateutil.tz.tzutc())
TIME_ZONE = zoneinfo.gettz("America/New_York")

def nano(val):
  """Converts a number to nano (str)."""
  return '%d' % (int(val) * 1e9)

def epoch_of_time_str(dateTimeStr, tzinfo):
  log_time = dateutil.parser.parse(dateTimeStr).replace(tzinfo=tzinfo)
  return (log_time - DAWN_TIME).total_seconds()

def read_steps_csv():
    print "Reading Steps"
    is_header = True
    steps = []
    with open('steps.csv', 'rb') as csvfile:
        steps_reader = csv.reader(csvfile, delimiter=',')
        for row in steps_reader:
            if is_header:
                is_header=False
                continue
            steps.append(dict(
                seconds_from_dawn=epoch_of_time_str(row[0], TIME_ZONE),
                steps=int(row[1])
                ))
    return steps

def read_steps_csv_with_gfit_format():
    steps = read_steps_csv()
    gfit_steps = []
    for step in steps:
        gfit_steps.append(dict(
            dataTypeName='com.google.step_count.delta',
            endTimeNanos=nano(step["seconds_from_dawn"] + 86399),
            startTimeNanos=nano(step["seconds_from_dawn"]),
            value=[dict(intVal=step["steps"])],
        ))
    return gfit_steps

if __name__=="__main__":
    gfit_steps = read_steps_csv_with_gfit_format()
