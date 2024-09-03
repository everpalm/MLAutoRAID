# Contents of test_ven_1b4b.py
'''Copyright (c) 2024 Jaron Cheng'''
from datetime import datetime
import logging
import pytest

logger = logging.getLogger(__name__)

class TestMLRampTime:

    FILE_NAME = 'ramp_times_vs_performance.png'

    @pytest.mark.dependency(name="prepare_data")
    def test_prepare_data(self, windows_ml_model):
        # Prepare data
        windows_ml_model.prepare_data()
        assert len(windows_ml_model.X_train) > 0,\
            "Training set should not be empty."
            
        assert len(windows_ml_model.y_train) > 0,\
                "Target set should not be empty."
        assert 'ramp_times' in windows_ml_model.X_train.columns,\
                "Feature 'ramp_times' should be in the training data."

    @pytest.mark.dependency(name="train_model", depends=["prepare_data"])
    def test_train_model(self, windows_ml_model):
        # Prepare data if the scope of windows_ml_model is function
        #windows_ml_model.prepare_data(10000)
        
        # Start training
        windows_ml_model.train_model()
        assert windows_ml_model.model is not None,\
                "Model should be trained and not be None."

    @pytest.mark.dependency(name="best_ramp_time", depends=["train_model"])
    def test_find_best_ramp_time(self, windows_ml_model):
        # Prepare data and training if scope of windows_ml_model is function
        #windows_ml_model.train_model()
        time_stamp = datetime.now().strftime('%Y%m%d%H%M%S')
        windows_ml_model.plot_results(f'logs\\{time_stamp}{self.FILE_NAME}')
        
        # Test and find best ramp_times
        best_ramp_time = windows_ml_model.find_best_ramp_time()
        assert best_ramp_time in range(1, windows_ml_model.range),\
                "Best ramp time should be within the expected range."

