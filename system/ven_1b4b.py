from abc import ABC, abstractmethod
import logging
import matplotlib.pyplot as plt
# from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
# from unit.mongodb import MongoDB as mdb

logger = logging.getLogger(__name__)


class MLModel(ABC):
    # def __init__(self, db_uri, db_name, collection_name, limit):
    def __init__(self, mongodb, range):
        # self.client = MongoClient(db_uri)
        # self.db = self.client[db_name]
        # self.collection = self.db[collection_name]
        # self.model = None
        self.mongodb = mongodb
        self.range = range + 1

    @abstractmethod
    def prepare_data(self):
        pass

    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def find_best_ramp_time(self):
        pass

class MLRampTime(MLModel):
    def prepare_data(self):
        # 提取数据并进行预处理
        # data = pd.DataFrame(list(self.collection.find()))
        # dict_raw_data = mdb('localhost', 27017, 'AutoRAID', 'amd_desktop').aggregate_ramp_metrics(self.limit)
        dict_raw_data = self.mongodb.aggregate_ramp_metrics()
        logger.info(f'self.range = {self.range}')
        logger.debug(f'type(raw_data) = {type(dict_raw_data)}')
        logger.debug(dict_raw_data['combined_data'])
        
        raw_data = dict_raw_data['combined_data']
        self.model = None

        data = pd.DataFrame(raw_data)
        logger.debug(f'data = {data}')
        
        # 假设目标是最大化 read_iops 和 write_iops，因此将其加和作为优化目标
        data['performance'] = data['read_iops'] + data['write_iops']

        # 选择特征和目标变量
        X = data[['ramp_times']]
        y = data['performance']
        # print(f'X = {X}')
        # print(f'y = {y}')
        # 划分训练集和测试集
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=0.5, random_state=42)

    def train_model(self):
        # 初始化并训练模型
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)

        # 评估模型
        predictions = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, predictions)
        logger.info(f'mse = {mse}')

    def find_best_ramp_time(self):
        # 生成可能的 ramp_times 值范围
        possible_ramp_times = pd.DataFrame({'ramp_times': range(1, self.range)})

        # predict performance
        performance_predictions = self.model.predict(possible_ramp_times)

        # Find best ramp_times
        best_index = performance_predictions.argmax()
        best_ramp_time = possible_ramp_times.iloc[best_index]['ramp_times']
        logger.info(f'best_ramp_time = {best_ramp_time}')
        return best_ramp_time

    def plot_results(self, save_path_with_timestamp):
        # 绘制 X 对 y 的曲线图
        plt.figure(figsize=(10, 6))
        plt.scatter(self.X_train, self.y_train, color='blue',
                    label='Training data')
        plt.scatter(self.X_test, self.y_test, color='green',
                    label='Testing data')
        plt.plot(self.X_test, self.model.predict(self.X_test), color='red',
                 label='Model prediction')
        plt.xlabel('Ramp Times')
        plt.ylabel('Performance')
        plt.title('Ramp Times vs Performance')
        plt.legend()
        # plt.show()
        plt.savefig(save_path_with_timestamp)

