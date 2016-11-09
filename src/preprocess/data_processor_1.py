import pandas as pd

def is_fraud(row):
    if row['acct_type'] in ['fraudster_event', 'fraudster', 'fraudster_att']:
        return True
    return False

def fraud_column(df):
    df['fraud'] = df.apply(lambda row: is_fraud(row), axis=1)
    return df

def event_creation_hours(df):
    df['event_creation_hours'] = (df.event_published - df.event_created)/float((60*60))
    return df

def previous_payout_count(df):
    df['previous_payout_count'] = df.apply(lambda row: len(row['previous_payouts']), axis=1)
    return df

def get_previous_payout_sum(row):
    result = 0
    for i in xrange(len(row['previous_payouts'])):
        result += row['previous_payouts'][i]['amount']
    return result

def previous_payout_sum(df):
    df['previous_payout_sum'] = df.apply(lambda row: get_previous_payout_sum(row), axis=1)
    return df

def run_data_processor_1(df, fraud=True):
    df_new = df
    if fraud:
        df_new = fraud_column(df)
    df_new = event_creation_hours(df_new)
    df_new = previous_payout_count(df_new)
    df_new = previous_payout_sum(df_new)
    return df_new

# def prev_address(row,address):
#     for i in xrange(len(row['previous_payouts'])):
#         if row['previous_payouts'] == address:
#             return True
#     return False
#
# def previous_event_at_address(df):
#     df['previous_event_at_address'] = df.apply(lambda row: prev_address(row,row['venue_address']), axis=1)
#     return df
