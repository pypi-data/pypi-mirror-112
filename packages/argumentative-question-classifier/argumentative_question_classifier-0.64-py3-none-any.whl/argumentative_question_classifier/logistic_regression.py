from argumentative_question_classifier.question_classifier import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import pickle
from sklearn.pipeline import Pipeline
import logging

class LogisticRegressionClassifier(QuestionClassifier):

    def __init__(self,features=None,c=None,max_iter=400):
        self.features=features
        self.c=c
        self.max_iter=max_iter
        self.spacy= spacy.load("ru_core_news_sm")

    def preprocess(self,df_questions):
        df_questions['parsed_question']=df_questions['question'].apply(lambda question: self.spacy(question))
        df_questions['questions-cleaned']=df_questions['parsed_question'].apply(lambda parsed_question: " ".join([token.text for token in parsed_question if not token.is_stop]))


    def build_model(self):
        tfidf = TfidfVectorizer(ngram_range=(1,4))
        logistic_regression = LogisticRegression(C=self.c,penalty='l2',solver='liblinear',max_iter=self.max_iter)
        pipeline = Pipeline([('tfidf',tfidf),('logistic-regression',logistic_regression)])
        return pipeline

    def fit(self,df_training):
        self.preprocess(df_training)
        self.model = self.build_model()
        labels=df_training['annotation']
        self.model.fit(df_training['questions-cleaned'].values,labels)

    def generate_paths(self,path):
        path_model=path+"/model.pkl"
        return  path_model

    def dump(self,path):
        path_model=self.generate_paths(path)
        with  open(path_model,'wb') as model_file:
            pickle.dump(self.model,model_file)

    def load(self,path):
        path_model=self.generate_paths(path)
        with open(path_model,'rb') as model_file:
            self.model= pickle.load(model_file)

    def predict_question(self,question):
        parsed_question = self.spacy(question)
        cleaned_question= " ".join([token.text for token in parsed_question if not token.is_stop])
        predictions=self.model.predict([cleaned_question])
        return predictions[0]

    def predict(self,df_test):
        self.preprocess(df_test)
        predicted_labels= self.model.predict(df_test['questions-cleaned'].values)
        return predicted_labels

    def __repr__(self):
        return f"Logistic Regression {self.c}"
