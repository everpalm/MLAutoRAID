from abc import ABC, abstractmethod
from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

class MLModel(ABC):
    def __init__(self, db_uri, db_name, collection_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.model = None

    @abstractmethod
    def prepare_data(self):
        pass

    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def find_best_ramp_time(self):
        pass

class WindowsMLModel(MLModel):
    def prepare_data(self):
        # 提取数据并进行预处理
        data = pd.DataFrame(list(self.collection.find()))

        # 假设目标是最大化 read_iops 和 write_iops，因此将其加和作为优化目标
        data['performance'] = data['read_iops'] + data['write_iops']

        # 选择特征和目标变量
        X = data[['ramp_times']]
        y = data['performance']

        # 划分训练集和测试集
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        # 初始化并训练模型
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)

        # 评估模型
        predictions = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, predictions)
        print(f'Mean Squared Error: {mse}')

    def find_best_ramp_time(self):
        # 生成可能的 ramp_times 值范围
        possible_ramp_times = pd.DataFrame({'ramp_times': range(1, 101)})

        # 预测性能
        performance_predictions = self.model.predict(possible_ramp_times)

        # 找到最佳 ramp_times
        best_index = performance_predictions.argmax()
        best_ramp_time = possible_ramp_times.iloc[best_index]['ramp_times']
        print(f'最佳 ramp times: {best_ramp_time}')
        return best_ramp_time

class MLModelFactory:
    @staticmethod
    def create_model(os_type, db_uri, db_name, collection_name):
        if os_type == "Windows":
            return WindowsMLModel(db_uri, db_name, collection_name)
        else:
            raise ValueError(f"Unsupported OS type: {os_type}")

# 使用工厂模式创建 Windows 的 ML 模型实例
if __name__ == "__main__":
    db_uri = 'mongodb://localhost:27017/'
    db_name = 'AutoRAID'
    collection_name = 'amd_desktop'

    model = MLModelFactory.create_model('Windows', db_uri, db_name, collection_name)
    model.prepare_data()
    model.train_model()
    model.find_best_ramp_time()
