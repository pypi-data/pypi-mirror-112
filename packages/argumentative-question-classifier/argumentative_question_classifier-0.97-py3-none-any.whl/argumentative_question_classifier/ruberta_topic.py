import logging

from argumentative_question_classifier.question_classifier import *
from simpletransformers.classification import ClassificationModel
import pandas as pd

class RubertaTopic(QuestionClassifier):

    def __init__(self,num_labels,path,from_dump=False,is_cuda_available=False):
        transformers_logger = logging.getLogger("transformers")
        transformers_logger.setLevel(logging.ERROR)
        transformers_logger.propagate = False
        self.num_labels=num_labels
        self.path=path
        self.is_cuda_available=is_cuda_available
        if from_dump:
            self.load_model()

    def rename_columns(self,df):
        df.rename(columns={'topic':'text_a','question':'text_b','annotation':'labels'},inplace=True)
        return df[['text_a','labels','text_b']]

    def fit(self,df_training):
        df_training=self.rename_columns(df_training)
        train_args={'reprocess_input_data': True, 'overwrite_output_dir': True,'num_train_epochs': 1,'best_model_dir':self.path,
                    'output_dir':self.path,
                    }
        self.model = ClassificationModel("bert", "DeepPavlov/rubert-base-cased", use_cuda=True,num_labels=self.num_labels,cuda_device=6,args=train_args)
        self.model.train_model(df_training,args=train_args)

    def predict(self,df_test):
        df_test=self.rename_columns(df_test.copy())
        test_topics = df_test['text_a'].values
        test_questions = df_test['text_b'].values
        test_dataset=[[pair[0],pair[1]] for pair in zip(test_topics,test_questions)]
        predicted_labels, outputs= self.model.predict(test_dataset)
        return predicted_labels

    def __repr__(self):
        return "Ruberta Topic"

    def load_model(self):
        self.model = ClassificationModel("bert",  self.path)