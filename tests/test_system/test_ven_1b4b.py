# Contents of test_ven_1b4b.py
'''Copyright (c) 2024 Jaron Cheng'''

import pytest

class TestWindowsMLModel:
    
    def test_prepare_data(self, windows_ml_model):
        # 测试数据准备步骤
        windows_ml_model.prepare_data()
        assert len(windows_ml_model.X_train) > 0, "Training set should not be empty."
        assert len(windows_ml_model.y_train) > 0, "Target set should not be empty."
        assert 'ramp_times' in windows_ml_model.X_train.columns, "Feature 'ramp_times' should be in the training data."

    def test_train_model(self, windows_ml_model):
        # 先准备数据
        windows_ml_model.prepare_data()
        
        # 测试模型训练步骤
        windows_ml_model.train_model()
        assert windows_ml_model.model is not None, "Model should be trained and not be None."

    def test_find_best_ramp_time(self, windows_ml_model):
        # 准备和训练模型
        windows_ml_model.prepare_data()
        windows_ml_model.train_model()
        # windows_ml_model.plot_results()
        
        # 测试找到最佳的 ramp_times
        best_ramp_time = windows_ml_model.find_best_ramp_time()
        assert best_ramp_time in range(1, 101), "Best ramp time should be within the expected range."

