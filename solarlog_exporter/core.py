from datetime import datetime
import logging
import os
from ftplib import FTP, error_perm
import socket
from time import sleep
from typing import Set

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from solarlog_exporter import file_handler, settings
from solarlog_exporter.file_handler import (get_last_record_time_influxdb, is_import_day_file, is_import_min_file)
from solarlog_exporter.parser import ConfigParser, DataParser

CHUNK_SIZE = 10000


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

    query_api = client.query_api()

    inverters = None
    last_record_time = get_last_record_time_influxdb(query_api, influx_bucket)
    client.close()
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
        if is_import_min_file(file, last_record_time):
            logging.debug("Read file %s", file)
            data_parser.parse_file(path + "/" + file)

    logging.debug("Daily and monthly data read..")

    # Store it in Influx DB
    datapoints = file_handler.chunks(
        inverters.get_inverter_datapoints_to_influx(), CHUNK_SIZE
    )
    client = InfluxDBClient(
        url=influx_host+":"+influx_port,
        token=influx_token,
        org=influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
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
    influx_token
):
    client = InfluxDBClient(
        url=influx_host+":"+influx_port,
        token=influx_token,
        org=influx_org)

    query_api = client.query_api()

    inverters = None
    last_record_time = get_last_record_time_influxdb(query_api, influx_bucket)
    client.close()
    logging.debug("Starting..")
    logging.debug("Used directory: %s", path)
    logging.debug("Last Record %s", last_record_time)

    if not settings.FTP_HOST:
        raise Exception("FTP_HOST not defined!")

    inverters = None
    try:
        with FTP(settings.FTP_HOST) as ftp:
            ftp.login(user=settings.FTP_USERNAME or "", passwd=settings.FTP_PASSWORD or "")
            ftp.sendcmd('OPTS UTF8 ON')

            # Read Configs at start
            config_parser = ConfigParser()
            config_parser.parse_ftp_file(ftp, path + "/base_vars.js")

            inverters, data_parser = createInvertersAndDataParsee(config_parser, last_record_time)

            importFileCounter = 0
            fileCounter = 0
            fileList = ftp.nlst(path)
            filteredMinFileList = list(filter(lambda filename: is_import_min_file(filename, last_record_time), fileList))
            filteredMinFileList.sort()
            filteredDayFileList = list(filter(lambda filename: is_import_day_file(filename, last_record_time), fileList))
            allFiles = filteredMinFileList + filteredDayFileList
            for file in allFiles:
                fileCounter += 1
                fileName = os.path.basename(file)
                logging.debug(f"Read file {fileName}. {fileCounter}/{len(fileList)}")
                data_parser.parse_ftp_file(ftp, path + "/" + fileName)
                importFileCounter += 1
                if importFileCounter >= 50:
                    writeDataToinfluxDb(inverters, influx_host, influx_port, influx_org, influx_bucket, influx_token)
                    importFileCounter = 0
                    inverters, data_parser = createInvertersAndDataParsee(config_parser, last_record_time)
            writeDataToinfluxDb(inverters, influx_host, influx_port, influx_org, influx_bucket, influx_token)
    except socket.error as e:
        if e.errno == 111:
            print("Connection refused. The FTP server may not be running.")
        else:
            print(f"Socket error: {e}")
        pass
    except error_perm as e:
        print(f"FTP permission error: {e}")
        pass
    except EOFError:
        print("EOFError: The connection was closed unexpectedly.")
        pass

def createInvertersAndDataParsee(config_parser, last_record_time):
    inverters = config_parser.get_inverters()
    if not inverters:
        raise Exception("No inverters in config found!")
    logging.debug("Inverters read from config..")
    data_parser = DataParser(inverters, last_record_time)
    return inverters, data_parser

def writeDataToinfluxDb(
        inverters,
        influx_host,
        influx_port,
        influx_org,
        influx_bucket,
        influx_token):
    # Store it in Influx DB
    datapoints = file_handler.chunks(
        inverters.get_inverter_datapoints_to_influx(), CHUNK_SIZE
    )
    client = InfluxDBClient(
        url=influx_host+":"+influx_port,
        token=influx_token,
        org=influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    influxCount = 0
    for chunk in datapoints:
        write_api.write(org=influx_org, bucket=influx_bucket, record=chunk)
        logging.debug("Datapoints in influxdb saved: %s", influxCount)
        influxCount += 1
    write_api.close()