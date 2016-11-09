import pandas as pd
from statsmodels.discrete.discrete_model import Logit
from scipy.stats.stats import pearsonr
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn.metrics import recall_score, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier
# import tyler_clean
import statsmodels.api as sm
# import data_processor_1 as dp
from sklearn.grid_search import GridSearchCV
import cPickle as pickle


def load_data(filename = 'data/data.json'):
    df = pd.read_json(filename)
    return df

def unique_account_types(df):
    return df.acct_type.unique()

def create_fraud_column(df):
    df['fraud'] = df['acct_type'] != 'premium'
    return df


def featurize(df,features):
    y = df['fraud']
    X = df[features]
    return X,y

def featurize_const(df,features):
    features.append('const')
    df['const'] = 1
    y = df['fraud']
    X = df[features]
    return X,y

def statsmodel_logit(X,y,features):
    X.all_caps_name = X.all_caps_name.apply(lambda x : 1 if x else 0)
    X.questionable_email_domain = X.questionable_email_domain.apply(lambda x : 1 if x else 0)
    model = Logit(y,sm.add_constant(X[features]))
    result = model.fit()
    return result

def train_test_split_(X,y,features):
    X_new = X[features]
    X_train, X_test, y_train, y_test = train_test_split(X_new,y)
    X_no_fraud = X_train[y_train == 0 ]
    y_no_fraud = y_train[y_train == 0]
    X_fraud = X_train[y_train == 1]
    y_fraud = y_train[y_train == 1 ]
    return X_no_fraud, X_no_fraud, X_fraud, y_fraud, X_test, y_test

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

    # def grid_search(self,n_cross,n_samp):
    #
    #     if self.model.__class__.__name__ == 'LogisticRegression':
    #         params_dict = {'C': [.1,1,10]}
    #     for value1 in params_dict[key1]:
    #         for value2 in params_dict[key2]




    def predict(self,X):
        self.prediction = self.model.predict(X)
        return self.prediction


    def predict_proba(self,X):
        self.proba = self.model.predict_proba(X)
        return self.proba



if __name__ == '__main__':
    df = load_data()
    #uniques = unique_account_types(df)
    #df = create_fraud_column(df)
    tyler_features = tyler_clean.clean(df)
    df = dp.run_data_processor_1(df)
    #doug_features = ['venue_country', 'country', 'body_length', 'fb_published', 'org_facebook',
    #'org_twitter', 'previous_payout_count', 'event_creation_hours', 'gts', 'has_logo',
    # 'name_length', 'previous_payout_sum', 'sale_duration2', 'venue_state', 'show_map']

    doug_features = ['previous_payout_sum','name_length','show_map']
    # facebook org
    # free tickets
    #
    features = ['fb_published','has_logo'] + tyler_features + doug_features
    #features.remove('')
    features.remove('ACH')
    y = df.pop('fraud')
    X = df

    X_no_fraud, X_no_fraud, X_fraud, y_fraud, X_test,y_test = train_test_split_(X,y,features)

    model_list = [LogisticRegression,GradientBoostingClassifier,AdaBoostClassifier,RandomForestClassifier]

    results = []
    for model in model_list:
        result = Models(model,X_no_fraud, X_no_fraud, X_fraud, y_fraud)
        result.cross_validate(5,1293)
        results.append(result)

    p = statsmodel_logit(X,y,features)
    p.summary()

    for result in results:
        with open(result.model.__class__.__name__ + '.pkl', 'w') as f:
            pickle.dump(result,f)
