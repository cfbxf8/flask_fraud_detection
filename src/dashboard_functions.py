from pymongo import MongoClient
import pandas as pd
import time
import matplotlib.pyplot as plt


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

    data['red_flags'] = nils(data)
    data['red_flags'] = data['red_flags'].map(lambda x: x.lstrip(','))

    table_columns = ['new_time', 'fraud_class', '_id', 'contact_info', 'red_flags']
    small_data = data[data['fraud_class']!= 'Unlikely'][table_columns]

    make_pie_chart(data)

    # small_data.sort()

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

def nils(df):
    blanks = check_blank(df)
    #email = check_email(df)
    check = check_check(df)
    logo = check_logo(df)
    total = blanks + ',' + check + ',' + logo
    total = total.replace(',,','')
    return total

def check_blank(df):
    check = df['payout_type'].map(lambda x: 'Flagged for blank payment' if x == '' else '')
    return check

def check_email(df):
    check = df['private_email_domain'].map(lambda x: ' Flagged for not having private email domain' if x == 0 else '')
    return check

def check_check(df):
    check = df['payout_type'].map(lambda x: ' Flagged for not having check payment' if x != 'CHECK' else '')
    return check

def check_logo(df):
    check = df['has_logo'].map(lambda x: ' Flagged for not having a logo ' if x == 0 else '')
    return check


def make_pie_chart(df):
   counts = df.fraud_class.value_counts()
   colors = ['g', '#F2B50F', '#FF0000', '#FFA500']
   plt.pie(counts, labels=counts.index, colors = colors)
   plt.savefig('/static/thing.jpg')

     

if __name__ == '__main__':
    data = dash_data(raw_table)