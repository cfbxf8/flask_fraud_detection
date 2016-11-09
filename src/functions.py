from pymongo import MongoClient
from pymongo import errors
import cPickle as pickle
import pandas as pd
import time
from Models import Models
from preprocess import tyler_clean
from preprocess import data_processor_1 as dp
from preprocess import cb


client = MongoClient()
db = client.scores
raw_table = db.raw
prediction_table = db.predictions


def unpickle_model(file_name):
    ''' Unpickle our models
    INPUT: file_name (str)
    OUTPUT: unpickled model
    '''
    with open('models/' + file_name) as f:
        curr_model = pickle.load(f)
    return curr_model


def update_db(jso, prediction, mongo_collection):
    '''Update DB based on objectid. Add in 
    prediction and timestamp.
    INPUT: json object, prediction (float), mongo_collection
    OUTPUT: None
    '''
    jso['predictions'] = prediction[1]
    jso['time_stamp'] = time.time()
    mongo_collection.update_one({"_id": jso['object_id']}, {
                                "$set": jso}, upsert=True)


def run_prediction(Model, jso):
    '''Run Prediction with our model, do preprocessing also.
    INPUT: unpickled Model, json object
    OUTPUT: prediction (float)
    '''
    X = add_features(jso)
    return Model.predict_proba(X)[0]


def add_features(jso):
    '''Convert json to df, do preprocessing and add features
    INPUT: json object
    OUTPUT: dataframe with added features
    '''
    df = pd.DataFrame.from_dict(jso, orient='index').T

    df['ticket_types'] = cb.dict_to_list(df['ticket_types'])
    df['previous_payouts'] = cb.dict_to_list(df['previous_payouts'])

    tyler_features = tyler_clean.clean(df)

    df = dp.run_data_processor_1(df, fraud=False)

    doug_features = ['previous_payout_sum','name_length','show_map']
    
    features = ['fb_published','has_logo'] + tyler_features + doug_features
    features.remove('ACH')
    
    X = df[features]
    return X
