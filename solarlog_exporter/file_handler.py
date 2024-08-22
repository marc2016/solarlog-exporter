import logging
import re
from datetime import datetime, timedelta, timezone

import pytz

from solarlog_exporter import settings
from solarlog_exporter.utils import MinDatapoint


def is_import_file(filename, last_record_time):
    pattern = r'min\d{6}\.js'
    if re.search(pattern, filename):
        date_str = filename[filename.index('min') + 3:filename.index('.js')]
        date = datetime.strptime(date_str, '%y%m%d')
        date = date.replace(tzinfo=timezone.utc)
        now = datetime.now()
        now = now.replace(tzinfo=timezone.utc)
        if date != now  and date >= last_record_time:
            return True
        

    if ('min_day.js' in filename or
        'days_hist.js' in filename or
        'days.js' in filename or
        re.search(r"^days.*\.js$", filename)):
        return True

    return False


def get_last_record_time_influxdb(query_api, influx_bucket):
    # query = "SELECT * FROM {} WHERE system = '{}' ORDER BY time DESC LIMIT 1;".format(
    #     MinDatapoint.influx_measurment_name, settings.SOLAR_LOG_NAME
    # )
    query = f'''
            from(bucket: "{influx_bucket}")
              |> range(start: 0)
              |> filter(fn: (r) => r._measurement == "{MinDatapoint.influx_measurment_name}" and r.system == "{settings.SOLAR_LOG_NAME}")
              |> sort(columns: ["_time"], desc: true)
              |> limit(n: 1)
            '''

    result_last_point_query = list(query_api.query(query))

    if result_last_point_query:
        time = result_last_point_query[0].records[0].values["_time"]
        logging.debug("Last record %s", time)
        return time

    # no last record found
    logging.warning("No last record found")
    return datetime(2000, 1,1)


def chunks(input_list, n):
    n = max(1, n)
    return (input_list[i : i + n] for i in range(0, len(input_list), n))
