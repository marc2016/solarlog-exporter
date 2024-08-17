from datetime import datetime
import logging
import os
from ftplib import FTP
from time import sleep
from typing import Set

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from solarlog_exporter import file_handler, settings
from solarlog_exporter.file_handler import (get_last_record_time_influxdb,
                                            is_import_file)
from solarlog_exporter.parser import ConfigParser, DataParser

CHUNK_SIZE = 100000


def start_import(
    path,
    influx_host,
    influx_port,
    influx_org,
    influx_bucket,
    influx_token
):
    client = InfluxDBClient(
        url=influx_host+":"+influx_port,
        token=influx_token,
        org=influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()

    inverters = None
    last_record_time = get_last_record_time_influxdb(query_api, influx_bucket)
    logging.debug("Starting..")
    logging.debug("Used directory: %s", path)
    logging.debug("Last Record %s", last_record_time)

    # Read Configs at start
    if os.path.exists(path + "/base_vars.js"):
        config_parser = ConfigParser()
        config_parser.parse_file(path + "/base_vars.js")
        inverters = config_parser.get_inverters()
        logging.debug("Inverters read from config..")
    else:
        raise Exception("No inverters in config found!")

    # Read Daily and Monthly Data
    data_parser = DataParser(inverters, last_record_time)
    for file in os.listdir(path):
        if is_import_file(file, last_record_time):
            logging.debug("Read file %s", file)
            data_parser.parse_file(path + "/" + file)

    logging.debug("Daily and monthly data read..")

    # Store it in Influx DB
    datapoints = file_handler.chunks(
        inverters.get_inverter_datapoints_to_influx(), CHUNK_SIZE
    )
    for chunk in datapoints:
        write_api.write(org=influx_org, bucket=influx_bucket, record=chunk)
        logging.debug("Datapoints in influxdb saved")
    write_api.close()


def start_ftp_import(
    path,
    influx_host,
    influx_port,
    influx_org,
    influx_bucket,
    influx_token,
    mon_for_changes=False
):
    client = InfluxDBClient(
        url=influx_host+":"+influx_port,
        token=influx_token,
        org=influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()

    inverters = None
    last_record_time = get_last_record_time_influxdb(query_api, influx_bucket)
    logging.debug("Starting..")
    logging.debug("Used directory: %s", path)
    logging.debug("Last Record %s", last_record_time)

    if not settings.FTP_HOST:
        raise Exception("FTP_HOST not defined!")

    inverters = None
    with FTP(settings.FTP_HOST) as ftp:
        ftp.login(user=settings.FTP_USERNAME or "", passwd=settings.FTP_PASSWORD or "")
        ftp.encoding='ISO-8859-1'
        ftp.sendcmd('OPTS UTF8 ON')

        # Read Configs at start
        config_parser = ConfigParser()
        config_parser.parse_ftp_file(ftp, path + "/base_vars.js")

        # Read Daily and Monthly Data
        if mon_for_changes:
            for add in changemon_ftp_directory(ftp, path):
                inverters = config_parser.get_inverters()
                if not inverters:
                    raise Exception("No inverters in config found!")
                logging.debug("Inverters read from config..")
                data_parser = DataParser(inverters, last_record_time)

                for file in add:
                    if is_import_file(file, last_record_time):
                        logging.debug("Read file %s", file)
                        data_parser.parse_ftp_file(ftp, path + "/" + file)

                logging.debug("Daily and monthly data read..")

                # Store it in Influx DB
                datapoints = file_handler.chunks(
                    inverters.get_inverter_datapoints_to_influx(), CHUNK_SIZE
                )
                influxCount = 0
                for chunk in datapoints:
                    write_api.write(org=influx_org, bucket=influx_bucket, record=chunk)
                    logging.debug("Datapoints in influxdb saved: %s", influxCount)
                    influxCount += 1
                write_api.close()
        else:
            inverters = config_parser.get_inverters()
            if not inverters:
                raise Exception("No inverters in config found!")
            logging.debug("Inverters read from config..")
            data_parser = DataParser(inverters, last_record_time)

            for file in ftp.nlst(path):
                fileName = os.path.basename(file)
                if is_import_file(fileName, last_record_time):
                    logging.debug("Read file %s", fileName)
                    data_parser.parse_ftp_file(ftp, path + "/" + fileName)

            logging.debug("Daily and monthly data read..")

    # Store it in Influx DB
    datapoints = file_handler.chunks(
        inverters.get_inverter_datapoints_to_influx(), CHUNK_SIZE
    )
    influxCount = 0
    for chunk in datapoints:
        write_api.write(org=influx_org, bucket=influx_bucket, record=chunk)
        logging.debug("Datapoints in influxdb saved: %s", influxCount)
        influxCount += 1
    write_api.close()


def changemon_ftp_directory(ftp: FTP, directory="./"):
    """Check ftp directory for file changes"""
    ls_prev: Set[str] = set()

    while True:
        ls = set(ftp.nlst(directory))

        # listen for new files
        add = ls - ls_prev

        # read current date again
        add.add('min_day.js')
        add.add('days.js')
        add.add('days_hist.js')

        if add:
            yield add

        ls_prev = ls
        sleep(20)
