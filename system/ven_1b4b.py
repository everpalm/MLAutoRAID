from abc import ABC, abstractmethod
import logging
import matplotlib.pyplot as plt
# from pymongo import MongoClient
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
# from unit.mongodb import MongoDB as mdb

logger = logging.getLogger(__name__)


class MLModel(ABC):

    def __init__(self, mongodb, range):
        self.mongodb = mongodb
        self.range = range + 1
        self.model = None
        self.dataframe = None

    @abstractmethod
    def prepare_data(self):
        pass

    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def find_best_value(self):
        pass

class MLRampTime(MLModel):
    
    def prepare_data(self):
        # 提取数据并进行预处理
        dict_raw_data = self.mongodb.aggregate_ramp_metrics(limit=10000)
        logger.info(f'self.range = {self.range}')
        logger.debug(f'type(raw_data) = {type(dict_raw_data)}')
        # logger.debug(dict_raw_data['combined_data'])
        
        raw_data = dict_raw_data['combined_data']

        dataframe = pd.DataFrame(raw_data)
        logger.debug(f'dataframe(type({type(dataframe)})) = {dataframe}')
        
        # 调用检查相关性的方法
        self.check_correlation(dataframe)

        # 假设目标是最大化 read_iops 和 write_iops，因此将其加和作为优化目标
        dataframe['performance'] = (dataframe['read_iops'] +
                                    dataframe['write_iops'])

        # 选择特征和目标变量
        X = dataframe[['ramp_times']]
        y = dataframe['performance']
        
        # 划分训练集和测试集
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=0.2, random_state=42)

    def check_correlation(self, data):
        # 計算相關係數矩陣
        corr_matrix = data.corr()
        logger.info(f'Correlation matrix:\n{corr_matrix}')

        # 繪製相關性熱圖
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix Heatmap')
        plt.savefig("logs\\heapmap_ramptime.png")

    def train_model(self):
        # 初始化并训练模型
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)

        # 评估模型
        predictions = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, predictions)
        logger.info(f'mse = {mse}')

    def find_best_value(self):
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


class MLStressMetric(MLModel):
    
    def prepare_data(self):
        # 提取数据并进行预处理
        dict_raw_data = self.mongodb.aggregate_stress_metrics(limit=10000)
        logger.info(f'self.range = {self.range}')
        logger.debug(f'type(raw_data) = {type(dict_raw_data)}')
        # logger.debug(dict_raw_data['combined_data'])
        
        raw_data = dict_raw_data['combined_data']

        dataframe = pd.DataFrame(raw_data)
        logger.debug(f'dataframe(type({type(dataframe)})) = {dataframe}')
        
        # 调用检查相关性的方法
        self.check_correlation(dataframe)

        # 假设目标是最大化 read_iops 和 write_iops，因此将其加和作为优化目标
        dataframe['performance'] = (dataframe['read_iops'] +
                                    dataframe['write_iops'])

        # 选择特征和目标变量
        X = dataframe[['io_depth']]
        y = dataframe['performance']
        
        # 划分训练集和测试集
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=0.2, random_state=42)

    def check_correlation(self, data):
        # 計算相關係數矩陣
        # corr_matrix = data.corr()
        # logger.info(f'Correlation matrix:\n{corr_matrix}')
        numeric_df = data.select_dtypes(include=[float, int])
        corr_matrix = numeric_df.corr()

        # 繪製相關性熱圖
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix Heatmap')
        plt.savefig("logs\\heapmap_stress.png")

    def train_model(self):
        # 初始化并训练模型
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)

        # 评估模型
        predictions = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, predictions)
        logger.info(f'mse = {mse}')

    def find_best_value(self):
        # 生成可能的 io_depth 值范围
        possible_io_depth = pd.DataFrame({'io_depth': range(1, self.range)})

        # predict performance
        performance_predictions = self.model.predict(possible_io_depth)

        # Find best ramp_times
        best_index = performance_predictions.argmax()
        best_io_depth = possible_io_depth.iloc[best_index]['io_depth']
        logger.info(f'best_io_depth = {best_io_depth}')
        return best_io_depth

    def plot_results(self, save_path):
        # 绘制 X 对 y 的曲线图
        plt.figure(figsize=(10, 6))
        plt.scatter(self.X_train, self.y_train, color='blue',
                    label='Training data')
        plt.scatter(self.X_test, self.y_test, color='green',
                    label='Testing data')
        plt.plot(self.X_test, self.model.predict(self.X_test), color='red',
                 label='Model prediction')
        plt.xlabel('I/O Depth')
        plt.ylabel('Performance')
        plt.title('I/O Depth vs Performance')
        plt.legend()
        # plt.show()
        plt.savefig(save_path)
