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

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

paramiko.util.log_to_file("paramiko.log", level=logging.CRITICAL)

logger = logging.getLogger(__name__)


# def pytest_addoption(parser):
#     parser.addoption(
#         "--mode",
#         action="store",
#         default="remote",
#         help="Default Mode: remote"
#     )
#     parser.addoption(
#         "--if_name",
#         action="store",
#         default="eth0",
#         help="Default name of interface: eth0"
#     )
#     parser.addoption(
#         "--config_file",
#         action="store",
#         default="app_map.json",
#         help="Default config file: app_map.json"
#     )
#     parser.addoption(
#         "--private_token",
#         action="store",
#         default="xxxxx-xxxx",
#         help="Check your GitLab Private Token"
#     )
# @pytest.fixture(scope="session")
# def cmdopt(request):
#     cmdopt_dic = {}
#     cmdopt_dic.update({'mode': request.config.getoption("--mode")})
#     cmdopt_dic.update({'if_name': request.config.getoption("--if_name")})
#     cmdopt_dic.update({'config_file': request.config.getoption("--config_file")})
#     cmdopt_dic.update({'private_token': request.config.getoption("--private_token")})
#     return cmdopt_dic


# @pytest.fixture(scope="session", autouse=True)
# def test_open_uart(drone):
#     print('\n\033[32m================ Setup UART ===============\033[0m')
#     yield drone.open_uart()
#     print('\n\033[32m================ Teardown UART ===============\033[0m')
#     drone.close_uart()

def pytest_sessionfinish(session, exitstatus):
    for item in session.items:
        test_folder = os.path.basename(os.path.dirname(item.fspath))
        collection_name = test_folder.replace('test_', '')
        mongo = MongoDB('192.168.0.128', 27017, 'MLAutoRAID', collection_name)
        for attr in MDB_ATTR:
            log_path = attr["Log Path"]
            report_path = attr["Report Path"]
            mongo.write_log_and_report(log_path, report_path)
