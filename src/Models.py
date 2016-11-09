import pandas as pd
from statsmodels.discrete.discrete_model import Logit
from scipy.stats.stats import pearsonr
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn.metrics import recall_score, accuracy_score


class Models(object):
    def __init__(self,model_name,X_no_fraud, y_no_fraud, X_fraud, y_fraud):
        self.model_name  = model_name
        self.X_no_fraud = X_no_fraud
        self.y_no_fraud = y_no_fraud
        self.X_fraud = X_fraud
        self.y_fraud = y_fraud



    def undersample(self,n_samp):
        X_samp = self.X_no_fraud.sample(n_samp)
        data = np.zeros((n_samp))
        y_samp = pd.Series(data)
        self.X_under_samp = pd.concat([X_samp,self.X_fraud])
        self.y_under_samp = pd.concat([y_samp,self.y_fraud])


    def cross_validate(self,n_cross,n_samp):
        self.model = self.model_name()
        recall_scores = []
        accuracy_scores = []
        for i in xrange(n_cross):
            self.undersample(n_samp)
            X_train, X_test, y_train,y_test = train_test_split(self.X_under_samp,self.y_under_samp)
            self.model.fit(X_train,y_train)
            y_predict= self.model.predict(X_test)
            accuracy = accuracy_score(y_test,y_predict)
            recall = recall_score(y_test,y_predict)
            recall_scores.append(recall)
            accuracy_scores.append(accuracy )
            self.accuracy = np.mean(accuracy_scores)
            self.recall = np.mean(recall_scores)

    def predict(self,X):
        self.prediction = self.model.predict(X)
        return self.prediction


    def predict_proba(self,X):
        self.proba = self.model.predict_proba(X)
        return self.proba


