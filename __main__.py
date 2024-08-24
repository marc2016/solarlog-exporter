import logging
import signal
import sys
import threading
import time

from solarlog_exporter import settings
from solarlog_exporter.core import start_ftp_import, start_import

def doImport():
    """
    Run main application with can interface
    """
    # Verbose output
    if settings.VERBOSE is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not settings.INFLUXDB_HOST or not settings.INFLUXDB_ORG or not settings.INFLUXDB_BUCKET:
        raise Exception('INFLUX_HOST or INFLUX_ORG or INFLUX_BUCKET not defined!')

    # scan directory
    # if settings.DIRECTORY:
    #     start_import(
    #         settings.DIRECTORY,
    #         influx_host=settings.INFLUXDB_HOST,
    #         influx_port=settings.INFLUXDB_PORT,
    #         influx_org=settings.INFLUXDB_ORG,
    #         influx_bucket=settings.INFLUXDB_BUCKET,
    #         influx_token=settings.INFLUXDB_TOKEN,
    #     )


    # scan with ftp
    if settings.FTP_DIRECTORY:
        start_ftp_import(
            settings.FTP_DIRECTORY,
            influx_host=settings.INFLUXDB_HOST,
            influx_port=settings.INFLUXDB_PORT,
            influx_org=settings.INFLUXDB_ORG,
            influx_bucket=settings.INFLUXDB_BUCKET,
            influx_token=settings.INFLUXDB_TOKEN,
            mon_for_changes=settings.FTP_MONITOR_FOR_CHANGES
        )

    # raise Exception('One env variable of DIRECTORY or FTP_DIRECTORY must be defined!')

e = threading.Event()

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True
    e.set()
    

if __name__ == '__main__':
  logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
  killer = GracefulKiller()
  while True:
    e.wait(timeout=600) 
    if killer.kill_now:
      break
    doImport()
    if killer.kill_now:
      break

  logging.info("End of the program. I was killed gracefully :)")
