from pymongo import MongoClient
import pandas as pd
import time

client = MongoClient()
db = client.scores
raw_table = db.raw

high_risk_threshold = 0.8
medium_risk_threshold = 0.5
low_risk_threshold = 0.2

def dash_data(mongo_collection):
    '''
    INPUT: mongo collection
    OUTPUT: pandas DataFrame

    the function takes in a mongo_collection and cleans it into
    a pandas DataFrame
    the array has 5 columns and n rows, the columns are timestamp,
    severity, eventid, contact info, and red flags. In that order.
    '''
    data = mongo_collection.find()
    data = pd.DataFrame(list(data))
    data['new_time'] = data['time_stamp'].apply(convert_time)

    data = get_classifications(data)

    email_prefix = 'first.last@'
    data['contact_info'] = email_prefix + data['email_domain']

    data['red_flags'] = 1

    table_columns = ['new_time', 'fraud_class', '_id', 'contact_info', 'red_flags']
    small_data = data[data['fraud_class']!= 'Unlikely'][table_columns]

    return small_data.values

def convert_time(one_time):
    new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(one_time))
    return new_time 

def classify_row(row):
   if row['predictions'] > high_risk_threshold:
       return 'High Risk'
   elif high_risk_threshold >= row['predictions'] > medium_risk_threshold:
       return 'Medium Risk'
   elif medium_risk_threshold >= row['predictions'] >= low_risk_threshold:
       return 'Low Risk'
   else:
       return 'Unlikely'

def get_classifications(df):
   df['fraud_class'] = df.apply(lambda row: classify_row(row), axis=1)
   return df
     

if __name__ == '__main__':
    data = dash_data(raw_table)