import pandas as pd
import numpy as np
import os

def isnumber(x):
    '''Function to check if a string contains a number'''
    try:
        float(x)
        return True
    except:
        return False

# Loop until a valid year is entered
invalid_input = True

while invalid_input:
    try:
        year = input('Enter a 4-digit year: ')
        if (int(year) < 1990) or (int(year) > 2009):
            raise ValueError('Enter a valid 4-digit year from 1981 to 2009.')
        invalid_input = False
    except:
        print('Enter a valid 4-digit year from 1981 to 2009.')

# Load HMDA data
hmda = pd.read_csv('hmda' + year + '.csv',
                   dtype={'respondent_id': 'str', 'agency_code': 'str', 'state_code': 'str', 'county_code': 'str',
                          'applicant_race': 'str', 'co_applicant_race': 'str',
                          'applicant_race_1': 'str', 'co_applicant_race_1': 'str',
                          'loan_amount': 'str', 'applicant_income': 'str'})


# Load HUD subprime lenders data
subprimes = pd.read_csv('subprime' + year + '.csv', dtype={'IDD': 'str', 'MH': 'str'})
subprimes.columns = ['idd', 'code', 'id', 'mh', 'name']


# Filter relevants states
data = hmda[hmda.state_code.isin(['01', '13', '27', '37', '45', '51'])].copy()

# Create lender idd
data['idd'] = data.agency_code + data.respondent_id

# Create new race categories
data['race_flag'] = 1 # 1: applicant and co-applicant are black

if int(year) < 2004:
    data.loc[(data.applicant_race != '3') & (data.co_applicant_race != '3'), 'race_flag'] = 2 # 2: other
    data.loc[(data.applicant_race == '5') & (data.co_applicant_race.isin(['5', '7', '8'])), 'race_flag'] = 3 # 3: white
    data.loc[(~data.applicant_race.isin(['1', '2', '3', '4', '5', '6'])) |
                 (~data.co_applicant_race.isin(['1', '2', '3', '4', '5', '6', '8'])), 'race_flag'] = 3 # 4: misreported

else:
    data.loc[(data.applicant_race_1 != '3') & (data.co_applicant_race_1 != '3'), 'race_flag'] = 2 # 2: other
    data.loc[(data.applicant_race_1 == '5') & (data.co_applicant_race_1.isin(['5', '7', '8'])), 'race_flag'] = 3 # 3: white
    data.loc[(~data.applicant_race_1.isin(['1', '2', '3', '4', '5', '6'])) |
                 (~data.co_applicant_race_1.isin(['1', '2', '3', '4', '5', '6', '8'])), 'race_flag'] = 3 # 4: misreported


# Select relevant columns
data = data.loc[:, ['as_of_year', 'idd', 'state_code', 'county_code', 'loan_type', 'loan_purpose',
                    'action_taken', 'race_flag', 'applicant_income', 'loan_amount']].copy()
data.loc[:, [
    'as_of_year', 'county_code', 'loan_type', 'loan_purpose', 'action_taken', 'race_flag', 'applicant_income', 'loan_amount']
        ] = data[data.loc[:, [
    'as_of_year', 'county_code', 'loan_type', 'loan_purpose', 'action_taken', 'race_flag', 'applicant_income', 'loan_amount']
        ].applymap(isnumber)]
data.applicant_income = data.applicant_income.astype('float64')
data.loan_amount = data.loan_amount.astype('float64')
#data.isna().sum()

data.loc[:, ['applicant_income', 'loan_amount']] = data.loc[
    :, ['applicant_income', 'loan_amount']
].fillna(data.loc[:, ['applicant_income', 'loan_amount']].mean())

data = data.dropna()
#data.isna().sum()


# Changing loan_type to multiple columns
data['conventional_loans'] = 0
data['FHA_loans']          = 0
data['VA_loans']           = 0
data['FSA_RHS_loans']      = 0

data.loc[data.loan_type == 1, 'conventional_loans'] = 1
data.loc[data.loan_type == 2, 'FHA_loans']          = 1
data.loc[data.loan_type == 3, 'VA_loans']           = 1
data.loc[data.loan_type == 4, 'FSA_RHS_loans']      = 1


# Changing loan_purpose to multiple columns
data['purchase']    = 0
data['improvement'] = 0
data['refinancing'] = 0
data['multifamily'] = 0

data.loc[data.loan_purpose == 1, 'purchase']    = 1
data.loc[data.loan_purpose == 2, 'improvement'] = 1
data.loc[data.loan_purpose == 3, 'refinancing'] = 1
data.loc[data.loan_purpose == 4, 'multifamily'] = 1


# Changing action_taken to multiple columns
data['loans_originated']              = 0
data['loans_approved_not_originated'] = 0
data['loans_denied']                  = 0
data['other_loans']                   = 0

data.loc[data.action_taken == 1, 'loans_originated']              = 1
data.loc[data.action_taken == 2, 'loans_approved_not_originated'] = 1
data.loc[data.action_taken == 3, 'loans_denied']                  = 1
data.loc[~data.action_taken.isin([1, 2, 3]), 'other_loans']       = 1


# Changing race_flag to multiple columns
data['race_black'] = 0
data['race_other'] = 0
data['race_white'] = 0
data['race_msrpd'] = 0

data.loc[data['race_flag'] == 1, 'race_black'] = 1
data.loc[data['race_flag'] == 2, 'race_other'] = 1
data.loc[data['race_flag'] == 3, 'race_white'] = 1
data.loc[data['race_flag'] == 4, 'race_msrpd'] = 1

# Add subprime flag
data = pd.merge(data, subprimes, on='idd', how='left')

data['subprime'] = 0

data.loc[data.mh.isin(['1']), 'subprime'] = 1

# Add subprime_originated column
data['subprime_originated'] = 0

data.loc[(data.action_taken == 1) & (data.subprime == 1), 'subprime_originated'] = 1

# Adding column for total amount of subprime loans
data['subprime_amount'] = 0

data.loc[data.subprime == 1, 'subprime_amount'] = data.loc[data.subprime == 1, 'loan_amount']

# Adding column for total amount of originated subprime loans
data['subprime_amount_originated'] = 0

data.loc[(data.action_taken == 1) & (data.subprime == 1), 'subprime_amount_originated'] = data.loc[
    (data.action_taken == 1) & (data.subprime == 1), 'loan_amount'
]

# Adding total column
data['total'] = 1

# Grouping data by state and year
state_data = (data.groupby(['as_of_year', 'state_code'])
              .agg({'applicant_income': 'sum', 'loan_amount': 'sum',
                  'conventional_loans': 'sum', 'FHA_loans': 'sum', 'VA_loans': 'sum', 'FSA_RHS_loans': 'sum',
                  'purchase': 'sum', 'improvement': 'sum', 'refinancing': 'sum', 'multifamily': 'sum',
                  'loans_originated': 'sum', 'loans_approved_not_originated': 'sum', 'loans_denied': 'sum', 'other_loans': 'sum',
                  'race_black': 'sum', 'race_other': 'sum', 'race_white': 'sum', 'race_msrpd': 'sum',
                  'subprime': 'sum', 'subprime_originated': 'sum', 'subprime_amount': 'sum', 'subprime_amount_originated': 'sum',
                  'total': 'sum'})
              .reset_index())

# Adding diff in diff dummy variable
state_data['did'] = 0

if int(year) >= 1999:
    state_data.loc[state_data.state_code == '37', 'did'] = 1

# Appending to CSV
state_data.to_csv('state_data.csv', mode='a', header=(not os.path.exists('state_data.csv')))

# Creating dataset with percentages
state_data_2 = state_data.copy()

for i in range(2, 22):
    state_data_2.iloc[:, i] = state_data_2.iloc[:, i] / state_data_2.total

state_data_2.iloc[:, 22] = state_data_2.iloc[:, 22] / state_data.subprime
state_data_2.iloc[:, 23] = state_data_2.iloc[:, 23] / state_data.subprime_originated

# Appending to CSV
state_data_2.to_csv('state_data_2.csv', mode='a', header=(not os.path.exists('state_data_2.csv')))


# Grouping data by state, county, and year
county_data = (data.groupby(['as_of_year', 'state_code', 'county_code'])
              .agg({'applicant_income': 'sum', 'loan_amount': 'sum',
                  'conventional_loans': 'sum', 'FHA_loans': 'sum', 'VA_loans': 'sum', 'FSA_RHS_loans': 'sum',
                  'purchase': 'sum', 'improvement': 'sum', 'refinancing': 'sum', 'multifamily': 'sum',
                  'loans_originated': 'sum', 'loans_approved_not_originated': 'sum', 'loans_denied': 'sum', 'other_loans': 'sum',
                  'race_black': 'sum', 'race_other': 'sum', 'race_white': 'sum', 'race_msrpd': 'sum',
                  'subprime': 'sum', 'subprime_originated': 'sum', 'subprime_amount': 'sum', 'subprime_amount_originated': 'sum',
                  'total': 'sum'})
              .reset_index())

# Adding diff in diff dummy variable
county_data['did'] = 0

if int(year) >= 1999:
    county_data.loc[county_data.state_code == '37', 'did'] = 1

# Appending to CSV
county_data.to_csv('county_data.csv', mode='a', header=(not os.path.exists('county_data.csv')))

# Creating dataset with percentages
county_data_2 = county_data.copy()

for i in range(3, 23):
    county_data_2.iloc[:, i] = county_data_2.iloc[:, i] / county_data_2.total

county_data_2.iloc[:, 23] = county_data_2.iloc[:, 23] / county_data.subprime
county_data_2.iloc[:, 24] = county_data_2.iloc[:, 24] / county_data.subprime_originated

# Appending to CSV
county_data_2.to_csv('county_data_2.csv', mode='a', header=(not os.path.exists('county_data_2.csv')))
