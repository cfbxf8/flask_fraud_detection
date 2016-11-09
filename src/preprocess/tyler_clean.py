import pandas as pd


def clean(df):
    '''
    INPUT: pandas data frame

    take in a dataframe of fraud data with known base columns and do feature engineering and cleaning
    '''
    init_cols = list(df.columns)
    ticket_types(df)

    # returns a list of all new columns
    return [col for col in df.columns if col not in init_cols]


def ticket_types(df):
    '''
    INPUT: pandas data frame
    '''
    create_free_ticket_column(
        df)  # makes a column 1 if there are free tickets

    # makes a column of the number of tickey ticket_types
    create_number_ticket_types_column(df)

    # makes a column 1 if the name of the event is in all caps
    create_title_all_caps_column(df)

    # fills na values in facebook and twitter org columns with 0
    fillna_facebook_twitter(df)

    # column that indicates that an email domain doesn't give out
    # email addresses publicly
    create_private_email_domain_column(df)

    # creates a column that indicates the email domain gives out
    # temporary email addresses, or isn't really a domain name
    create_questionable_email_domain_column(df)

    dummy_payout_type(df)  # makes dummies of the payout_type column

    # column is a count of the available tickets for the event
    create_tickets_available_column(df)
    pass


def create_number_ticket_types_column(df):
    df['num_ticket_types'] = df['ticket_types'].map(_num_tickets)


def create_free_ticket_column(df):
    df['free_ticket_type'] = df['ticket_types'].map(_free_ticket)


def create_title_all_caps_column(df):
    df['all_caps_name'] = df['name'].map(_all_caps)


def fillna_facebook_twitter(df):
    df['org_facebook'].fillna(0, inplace=True)
    df['org_twitter'].fillna(0, inplace=True)


def create_private_email_domain_column(df):
    df['private_email_domain'] = df[
        'email_domain'].map(_private_public)


def create_questionable_email_domain_column(df):
    df['questionable_email_domain'] = df[
        'email_domain'].map(_questionable_email_domain)


def dummy_payout_type(df):
    dummies = pd.get_dummies(df['payout_type'])
    for col in ['', 'ACH', 'CHECK']:
        try:
            df[col] = dummies[col]
        except KeyError:
            df[col] = 0


def create_tickets_available_column(df):
    df['tickets_available'] = df['ticket_types'].map(_count_tickets)
    pass


def _num_tickets(lst):
    return len(lst)


def _free_ticket(lst):
    for d in lst:
        if d['cost'] == 0:
            return 1
    return 0


def _all_caps(name):
    return name.upper() == name


def _private_public(name):
    public = ['gmail.com', 'live.com', 'me.com', 'ymail.com',
              'comcast.net', 'live.fr', 'sbcglobal.net', 'mac.com', 'msn.com', 'live.co.uk', 'rocketmail.com', 'verizon.net',
              'googlemail.com', 'cox.net', 'outlook.com', 'att.net', 'telus.net', 'bellsouth.net', 'icloud.com', 'aim.com']
    common = ['yahoo', 'aol', 'hotmail']
    if name.split('.')[0].lower() in common:
        return 0
    return int(name.lower() not in public)


def _questionable_email_domain(name):
    questionable = ['yopmail.com', '.com',
                    'throwawaymail.com', 'mytemp.email', 'guerillamail.com']
    return name.lower() in questionable


def _count_tickets(lst):
    count = 0
    for d in lst:
        count += d['quantity_total']
    return count

if __name__ == '__main__':
    df = pd.read_json('../data/subset.json')
    clean(df)
    df.info()
