'''Copyright (c) 2024 Jaron Cheng'''
import pytest
import logging
import os
import paramiko
from unit.mongodb import MongoDB

MDB_ATTR = [{
    "Log Path": 'logs/test.log',
    "Report Path": ".report.json"
}]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
paramiko.util.log_to_file("paramiko.log", level=logging.CRITICAL)

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--ip",
        action="store",
        default="192.168.0.128",
        help="Default IP: 192.168.0.128"
    )
    parser.addoption(
        "--port",
        action="store",
        default="27017",
        help="Default port: 27017"
    )
    parser.addoption(
        "--database",
        action="store",
        default="AutoRAID",
        help="Default database: AutoRAID"
    )
    parser.addoption(
        "--collection",
        action="store",
        default="amd64",
        help="Default collection: amd64"
    )


@pytest.fixture(scope="session")
def cmdopt(request):
    cmdopt_dic = {}
    cmdopt_dic.update({'ip': request.config.getoption("--ip")})
    cmdopt_dic.update({'port': request.config.getoption("--port")})
    cmdopt_dic.update({'database': request.config.getoption("--database")})
    cmdopt_dic.update({'collection': request.config.getoption("--collection")})
    return cmdopt_dic


def pytest_sessionfinish(session, exitstatus):
    for item in session.items:
        test_folder = os.path.basename(os.path.dirname(item.fspath))
        collection_name = test_folder.replace('test_', '')
        mongo = MongoDB('192.168.0.128', 27017, 'MLAutoRAID', collection_name)
        for attr in MDB_ATTR:
            log_path = attr["Log Path"]
            report_path = attr["Report Path"]
            mongo.write_log_and_report(log_path, report_path)
