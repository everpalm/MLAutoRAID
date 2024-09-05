# Content of conftest.py
'''Copyright (c) 2024 Jaron Cheng'''

import pytest
# from system.ven_1b4b import MLModelFactory
# from unittest.mock import MagicMock
from system.ven_1b4b import MLRampTime
from system.ven_1b4b import MLStressMetric
from unit.mongodb import MongoDB

@pytest.fixture(scope='module', autouse=True)
def mdb():
    print('\n\033[32m================ Setup MongoDB ========\033[0m')
    db_ip = '192.168.0.128'
    db_port = 27017
    db_name = 'AutoRAID'
    collection_name = 'amd_desktop'
    print(f'db_ip = {db_ip}')
    print(f'db_port = {db_port}')
    print(f'db_name = {db_name}')
    print(f'collection_name = {collection_name}')
    return MongoDB(db_ip, db_port, db_name, collection_name)

@pytest.fixture(scope='module', autouse=True)
def windows_ramp_model(mdb):
    print('\n\033[32m================ Setup ML Ramp Time ============\033[0m')
    return MLRampTime(mdb, range=180)

@pytest.fixture(scope='module', autouse=True)
def windows_stress_model(mdb):
    print('\n\033[32m================ Setup ML Stress Model =========\033[0m')
    return MLStressMetric(mdb, range=32)