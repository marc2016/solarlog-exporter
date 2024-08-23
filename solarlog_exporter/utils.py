from operator import itemgetter
import re
from abc import abstractmethod
from datetime import datetime
from typing import Optional

import pytz as pytz

from solarlog_exporter import settings


class FileType:
    """
    File Types for SolarLog datas
    """

    MIN = 1
    DAY = 2
    MONTH = 3
    YEAR = 4
    MIN_STR = 5

    @staticmethod
    def get_filetype(line):
        if line.startswith("m[mi++]="):
            return FileType.MIN
        elif line.startswith("da[dx++]="):
            return FileType.DAY
        else:
            return None


class Inverter:
    """
    Inverter Object
    """

    def __init__(self, inverter_config, system):
        self.datapoints_min = {}
        self.datapoints_day = {}
        self.datapoints_string = {}
        if len(inverter_config) > 2:
            for str in inverter_config[2]:
                self.datapoints_string[str] = {}
        else:
            self.datapoints_string["String 1"] = {}

        self.name = inverter_config[0][4]
        self.system = system
        if re.match(r"WR \d*", self.name):
            self.name = self.name[:3] + self.name[3:].zfill(2)
        self.type = inverter_config[0][0]
        self.power = inverter_config[0][2]
        if len(inverter_config) > 1 and inverter_config[1] != None:
            self.group = inverter_config[1]
        else:
            self.group = 'nogroup'

    def add_datapoint(self, datapoint, last_record_time):
        if datapoint.date_time.date() < last_record_time.date():
            return

        if datapoint.type == FileType.MIN:
            self.datapoints_min[datapoint.get_date_time_as_timestring()] = datapoint
        if datapoint.type == FileType.MIN_STR:
            self.datapoints_string[datapoint.name][datapoint.get_date_time_as_timestring()] = datapoint
        elif datapoint.type == FileType.DAY:
            self.datapoints_day[datapoint.get_date_time_as_datestring()] = datapoint

    def get_datapoints_to_influx(self):
        influx_datapoints = []

        for _, value in self.datapoints_min.items():
            influx_datapoints.append(value.get_datapoint_to_influx(self))

        for key, value in self.datapoints_string.items():
            for k,v in value.items():
                influx_datapoints.append(v.get_datapoint_to_influx(self))

        for _, value in self.datapoints_day.items():
            influx_datapoints.append(value.get_datapoint_to_influx(self))

        return influx_datapoints



class InverterList:
    """
    List of all inverters found in the config
    """

    def __init__(self, inverter_config, system):
        self.inverters = []

        if len(inverter_config) == 0:
            raise ValueError("No inverter in config found")

        if not system:
            raise ValueError("No name of system provided")

        for inverter in inverter_config:
            self.inverters.append(Inverter(inverter, system))

    def get_inverter(self, key) -> Optional[Inverter]:
        if key < 0 or key >= self.get_number_of_inverters():
            return None
        return self.inverters[key]

    def get_number_of_inverters(self):
        return len(self.inverters)

    def get_inverter_datapoints_to_influx(self):
        datapoints = []

        for inverter in self.inverters:
            datapoints += inverter.get_datapoints_to_influx()

        return datapoints


class Datapoint:
    """
    Basic Datapoint
    """

    _timezone = pytz.timezone(settings.TIMEZONE)
    date_time = datetime.now()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.date_time == other.date_time

    @abstractmethod
    def get_datapoint_to_influx(self, inverter):
        pass

    def get_date_time_as_timestring(self):
        return self.date_time.strftime("%d.%m.%y %H:%M:%S")

    def get_date_time_as_datestring(self):
        return self.date_time.date().strftime("%d.%m.%y")

    def get_date_time_for_influxdb(self):
        return self.date_time.astimezone(pytz.utc).isoformat().replace("+00:00", "Z")


class MinDatapoint(Datapoint):
    """
    Minute Datapoint (min_xxxx.js)
    """

    influx_measurment_name = "solarlog_min"
    type = FileType.MIN

    def __init__(self, min_time, pac, eday, temperature):
        self.date_time = self._timezone.localize(
            datetime.strptime(min_time, "%d.%m.%y %H:%M:%S")
        )
        self.pac = 0 if not pac else float(pac)
        self.eday = 0 if not eday else float(eday)
        self.temperature = 0 if not temperature else int(temperature)

    def get_datapoint_to_influx(self, inverter):
        return {
            "measurement": self.influx_measurment_name,
            "tags": {
                "inverter": inverter.name,
                "system": inverter.system,
                "group": inverter.group,
            },
            "time": self.get_date_time_for_influxdb(),
            "fields": {
                "Pac": self.pac,
                "Eday": self.eday,
                "temperature": self.temperature,
            },
        }


class DayDatapoint(Datapoint):
    """
    Day Datapoint (days.js, days_hist.js)
    """

    influx_measurment_name = "solarlog_day"
    type = FileType.DAY

    def __init__(self, day_time, eday, pac_max):
        self.date_time = self._timezone.localize(
            datetime.strptime(day_time, "%d.%m.%y")
        )
        self.eday = 0 if not eday else float(eday)
        self.pac_max = 0 if not pac_max else float(pac_max)

    def get_datapoint_to_influx(self, inverter):
        return {
            "measurement": self.influx_measurment_name,
            "tags": {
                "inverter": inverter.name,
                "system": inverter.system,
                "group": inverter.group,
            },
            "time": self.get_date_time_for_influxdb(),
            "fields": {"Eday": self.eday, "PacMax": self.pac_max},
        }

class StringDatapoint(Datapoint):
    """
    String Datapoint (String data from min_xxxx.js)
    """

    influx_measurment_name = "solarlog_min_strings"
    type = FileType.MIN_STR

    def __init__(self, min_time, name, pdc, udc):
        self.date_time = self._timezone.localize(
            datetime.strptime(min_time, "%d.%m.%y %H:%M:%S")
        )
        self.pdc = 0 if not pdc else float(pdc)
        self.udc = 0 if not udc else float(udc)
        self.name = name

    def get_datapoint_to_influx(self, inverter):
        return {
            "measurement": self.influx_measurment_name,
            "tags": {
                "inverter": inverter.name,
                "system": inverter.system,
                "group": inverter.group,
                "string": self.name
            },
            "time": self.get_date_time_for_influxdb(),
            "fields": {
                "Pdc": self.pdc,
                "Udc": self.udc,
            },
        }