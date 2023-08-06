from abc import abstractmethod
import pandas as pd
class QuestionClassifier:

    def rename_columns(self,df):
        df.rename(columns={'question':'text','annotation':'labels'},inplace=True)
        return df[['text','labels',]]

    @abstractmethod
    def fit (self,train_dataset):
        pass

    @abstractmethod
    def predict(self,test_dataset):
        pass

    @abstractmethod
    def dump(self,path):
        pass



    @abstractmethod
    def load(self,path):
        pass