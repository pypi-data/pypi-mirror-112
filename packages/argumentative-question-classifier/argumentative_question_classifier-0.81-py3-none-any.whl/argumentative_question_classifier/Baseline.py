from argumentative_question_classifier.question_classifier import *
import numpy as np
class RandomBaseline(QuestionClassifier):
    def __init__(self,labels):
        self.labels=labels

    def __int__(self,path):
        pass

    def fit(self,train_dataset):
        None

    def predict(self,test_dataset):
        return [np.random.choice(self.labels,1,True)[0] for sentence in range(0,test_dataset.shape[0])]


    def __repr__(self):
        return "Random Baseline"


class MajorityBaseline(QuestionClassifier):
    def __init__(self):
        pass

    def __int__(self,path):
        pass

    def fit(self,train_dataset):
        None

    def predict(self,test_dataset):
        return [0 for sentence in range(0,test_dataset.shape[0])]


    def __repr__(self):
        return "Majority Baseline"