from argumentative_question_classifier.question_classifier import *
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import logging

class SVM(QuestionClassifier):

    def __init__(self,features=None,c=None,max_iter=400):
        self.features=features
        self.c=c
        self.max_iter=max_iter
        self.spacy= spacy.load("ru_core_news_sm")

    def preprocess(self,df_questions):
        df_questions['parsed_question']=df_questions['question'].apply(lambda question: self.spacy(question))
        df_questions['questions-cleaned']=df_questions['parsed_question'].apply(lambda parsed_question: " ".join([token.text for token in parsed_question if not token.is_stop]))

    def build_feature_space(self,df_training):
        self.preprocess(df_training)
        self.feature_space=TfidfVectorizer(ngram_range=(1,4))
        self.feature_space.fit(df_training['questions-cleaned'].values)

    def extract_feature_vectors(self,df_questions):
        self.preprocess(df_questions)
        feature_vectors=self.feature_space.transform(df_questions['questions-cleaned'].values)
        return feature_vectors

    def fit(self,df_training):
        self.build_feature_space(df_training)
        feature_vector=self.extract_feature_vectors(df_training)
        labels=df_training['annotation']
        self.model= LinearSVC(C=self.c,loss='hinge')
        self.model.fit(feature_vector,labels)

    def predict(self,df_test):
        feature_vector=self.extract_feature_vectors(df_test)
        predicted_labels= self.model.predict(feature_vector)
        return predicted_labels

    def __repr__(self):
        return f"SVM {self.c}"
