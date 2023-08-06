"""
This module implements a mechanism to log monitoring data to an InfluxDB database.

The database connection has to be established once and can then be used from the entire project.
"""
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from influxdb import InfluxDBClient

import yaml
from rettij.common.logging_utilities import LoggingSetup


class _MonitoringLogger:
    """
    Logger used for writing monitoring data to an InfluxDB database.
    """

    def __init__(self, config_file_path: Optional[Path] = None) -> None:
        """
        Create a new MonitoringLogger using the InfluxDB client.

        :param config_file_path: InfluxDB client configuration file path. File has to be in YAML format. Keys:
            - address (Default: 'localhost')
            - port (Default: '8086')
            - username (Default: 'root')
            - password (Default: 'root')
            - database (Default: 'rettij')
            - ssl (Default: 'False')
            - verify_ssl (Default: 'False')
        """
        if config_file_path:
            if not config_file_path.exists():
                raise FileNotFoundError(config_file_path)
            with open(config_file_path, "r") as fd:
                config = yaml.load(fd)
        else:
            config = {}

        self.db_address: str = config.get("address", "localhost")
        self.db_port: int = config.get("port", 8086)
        self.db_username: str = config.get("username", "root")
        self.db_password: str = config.get("password", "root")
        self.db_name: str = config.get("database", "rettij")
        self.db_use_ssl: bool = config.get("ssl", False)
        self.db_verify_ssl: bool = config.get("verify_ssl", False)

        self.logger = LoggingSetup.submodule_logging(self.__class__.__name__)

        self.logger.debug(
            "Creating InfluxDB database client with "
            f"host={self.db_address}, "
            f"port={self.db_port}, "
            f"username={self.db_username}, "
            f"password={self.db_password}, "
            f"database={self.db_name}, "
            f"ssl={self.db_use_ssl}, "
            f"verify_ssl={self.db_verify_ssl}"
        )

        self.db_client = InfluxDBClient(
            host=self.db_address,
            port=self.db_port,
            username=self.db_username,
            password=self.db_password,
            database=self.db_name,
            ssl=self.db_use_ssl,
            verify_ssl=self.db_verify_ssl,
        )

    def log(self, measurement: str, entity_name: str, attr_name: str, attr_value: Union[int, str]) -> None:
        """
        Log the supplied data with the current time as timestamp.

        :param measurement: Type of measurement (i.e. Node type)
        :param entity_name: Entity that created the measurement
        :param attr_name: Attribute that is measured
        :param attr_value: Value of the measured attribute
        """
        iso_time = datetime.datetime.now().isoformat()

        values: List[Dict[str, Any]] = [
            {
                "measurement": measurement,
                "time": iso_time,
                "tags": {"user": "rettij", "entity_name": entity_name},
                "fields": {attr_name: attr_value},
            }
        ]
        self.db_client.write_points(values)
        self.logger.debug(f"Wrote values to InfluxDB: {values}")

        # values = [{ "measurement": "TEST", "time": datetime.datetime.now().isoformat(), "tags": {"user": "test", "entity_name": "test"}, "fields": {"test-attr": "abcdef"} }]
        # query = 'SELECT * FROM "test"."autogen"."TEST"'


monitoring_logger: Optional[_MonitoringLogger] = None
active: bool = False


def get_logger(config_file_path: Optional[Path] = None) -> _MonitoringLogger:
    """
    Retrieve the monitoring logger.

    :param config_file_path: Configuration for the initial logger setup.
    :return: New MonitoringLogger on the first call, existing object on successive calls.
    """
    global monitoring_logger
    global active
    if not monitoring_logger:
        monitoring_logger = _MonitoringLogger(config_file_path)
        active = True

    return monitoring_logger


def log(measurement: str, entity_name: str, attr_name: str, attr_value: Union[int, str]) -> None:
    """
    Log a monitoring message using the MonitoringLogger class.

    :param measurement: Type of measurement (i.e. Node type)
    :param entity_name: Entity that created the measurement
    :param attr_name: Attribute that is measured
    :param attr_value: Value of the measured attribute
    """
    if active:
        get_logger().log(measurement, entity_name, attr_name, attr_value)
