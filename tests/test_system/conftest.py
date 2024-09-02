# Content of conftest.py
'''Copyright (c) 2024 Jaron Cheng'''

import pytest
# from system.ven_1b4b import MLModelFactory
# from unittest.mock import MagicMock
from system.ven_1b4b import WindowsMLModel as wmlm
# from unit.mongodb import MongoDB as mdb

@pytest.fixture
def windows_ml_model():
    # 使用工厂创建一个Windows的ML模型实例
    # db_uri = 'mongodb://localhost:27017/'
    # db_ip = 'localhost'
    # db_name = 'AutoRAID'
    # collection_name = 'amd_desktop'
    # db_port = 27017

    # model = MLModelFactory.create_model('Windows', db_uri, db_name, collection_name)
    # model = mdb(db_ip, db_port, db_name, collection_name)
    # # Mock 数据库集合以避免实际数据库调用
    # model.collection = MagicMock()

    # # 提供伪数据供测试
    # model.collection.find.return_value = [
    #     {'ramp_times': 10, 'read_iops': 1500, 'write_iops': 1300, 'read_bw': 500, 'write_bw': 450},
    #     {'ramp_times': 20, 'read_iops': 1600, 'write_iops': 1350, 'read_bw': 520, 'write_bw': 470},
    #     {'ramp_times': 30, 'read_iops': 1700, 'write_iops': 1400, 'read_bw': 540, 'write_bw': 490},
    # ]

    # return model
    print('\n\033[32m================ Setup Windows ML Model ========\033[0m')
    return wmlm('192.168.0.128', 'AutoRAID', 'amd_desktop', 10000)