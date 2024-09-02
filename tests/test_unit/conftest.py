# Content of conftest.py
'''Copyright (c) 2024 Jaron Cheng'''

import pytest
import logging
from unittest.mock import patch
from unit.mongodb import MongoDB

logging.getLogger("pymongo").setLevel(logging.CRITICAL)
logging.getLogger('unit.mongodb').setLevel(logging.INFO)
# logger = logging.getLogger(__name__)

                
@pytest.fixture(scope="module")
def mongo_db():
    # Mock MongoDB client
    mock_client = patch('unit.mongodb.MongoClient').start()
    mock_db = mock_client.return_value['test_db']
    mock_collection = mock_db['test_collection']

    # Create instance of MongoDB class
    mongo_db_instance = MongoDB('localhost', 27017, 'test_db', 'test_collection')
    
    yield mongo_db_instance, mock_collection    
    patch.stopall()
