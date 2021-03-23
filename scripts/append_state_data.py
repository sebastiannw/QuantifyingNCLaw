import pandas as pd
import numpy as np
import os

# Loading aggregated hmda data

state_data = pd.read_csv('../data/aggregated/state_data.csv',
                         dtype={'as_of_year': 'int', 'state_code': 'int',
                                'applicant_income': 'float', 'loan_amount': 'float',
                                'conventional_loans': 'int', 'FHA_loans': 'int',
                                'VA_loans': 'int', 'FSA_RHS_loans': 'int',
                                'purchase': 'int', 'improvement': 'int',
                                'refinancing': 'int', 'multifamily': 'int',
                                'loans_originated': 'int', 'loans_approved_not_originated': 'int',
                                'loans_denied': 'int', 'other_loans': 'int',
                                'race_black': 'int', 'race_other': 'int',
                                'race_white': 'int', 'race_msrpd': 'int',
                                'subprime': 'int', 'subprime_originated': 'int',
                                'subprime_amount': 'float', 'subprime_amount_originated': 'float',
                                'total': 'int'}).iloc[:, 1:]

state_relative = pd.read_csv('../data/aggregated/state_relative.csv',
                             dtype={'as_of_year': 'int', 'state_code': 'int',
                                    'applicant_income': 'float', 'loan_amount': 'float',
                                    'conventional_loans': 'float', 'FHA_loans': 'float',
                                    'VA_loans': 'float', 'FSA_RHS_loans': 'float',
                                    'purchase': 'float', 'improvement': 'float',
                                    'refinancing': 'float', 'multifamily': 'float',
                                    'loans_originated': 'float', 'loans_approved_not_originated': 'float',
                                    'loans_denied': 'float', 'other_loans': 'float',
                                    'race_black': 'float', 'race_other': 'float',
                                    'race_white': 'float', 'race_msrpd': 'float',
                                    'subprime': 'float', 'subprime_originated': 'float',
                                    'subprime_amount': 'float', 'subprime_amount_originated': 'float',
                                    'total': 'int'}).iloc[:, 1:]

county_data = pd.read_csv('../data/aggregated/county_data.csv',
                          dtype={'as_of_year': 'int', 'state_code': 'int', 'county_code': 'int',
                                 'applicant_income': 'float', 'loan_amount': 'float',
                                 'conventional_loans': 'int', 'FHA_loans': 'int',
                                 'VA_loans': 'int', 'FSA_RHS_loans': 'int',
                                 'purchase': 'int', 'improvement': 'int',
                                 'refinancing': 'int', 'multifamily': 'int',
                                 'loans_originated': 'int', 'loans_approved_not_originated': 'int',
                                 'loans_denied': 'int', 'other_loans': 'int',
                                 'race_black': 'int', 'race_other': 'int',
                                 'race_white': 'int', 'race_msrpd': 'int',
                                 'subprime': 'int', 'subprime_originated': 'int',
                                 'subprime_amount': 'float', 'subprime_amount_originated': 'float',
                                 'total': 'int'}).iloc[:, 1:]

county_relative = pd.read_csv('../data/aggregated/county_relative.csv',
                              dtype={'as_of_year': 'int', 'state_code': 'int', 'county_code': 'int',
                                     'applicant_income': 'float', 'loan_amount': 'float',
                                     'conventional_loans': 'float', 'FHA_loans': 'float',
                                     'VA_loans': 'float', 'FSA_RHS_loans': 'float',
                                     'purchase': 'float', 'improvement': 'float',
                                     'refinancing': 'float', 'multifamily': 'float',
                                     'loans_originated': 'float', 'loans_approved_not_originated': 'float',
                                     'loans_denied': 'float', 'other_loans': 'float',
                                     'race_black': 'float', 'race_other': 'float',
                                     'race_white': 'float', 'race_msrpd': 'float',
                                     'subprime': 'float', 'subprime_originated': 'float',
                                     'subprime_amount': 'float', 'subprime_amount_originated': 'float',
                                     'total': 'int'}).iloc[:, 1:]

# Population data management
population_data = pd.read_csv('../data/population/state_pop2.csv',
                              dtype={'year': 'int', 'state': 'str',
                                     'state_fips': 'int', 'county_fips': 'int',
                                     'race': 'int', 'sex': 'int',
                                     'age': 'int', 'population': 'int',
                                     'total_population': 'int', 'percent_population': 'float64'}).iloc[:, 1:]

# Filter data by years
population_data = population_data[(population_data.year >= 1990) & (population_data.year <= 2006)]
population_data = population_data[population_data.state.isin(['AL', 'GA', 'MN', 'NC', 'SC', 'VA'])]

# Extract aggregate stats
state_population = population_data.groupby(['year', 'state'])['population'].sum().reset_index()
#county_population = population_data.groupby(['year', 'state', 'county_fips'])['population'].sum().reset_index()

# HPI data management
hpi_AL = pd.read_csv('../data/hpi/ALSTHPI.csv', names=['date', 'sthpi'], header=0)
hpi_GA = pd.read_csv('../data/hpi/GASTHPI.csv', names=['date', 'sthpi'], header=0)
hpi_MN = pd.read_csv('../data/hpi/MNSTHPI.csv', names=['date', 'sthpi'], header=0)
hpi_NC = pd.read_csv('../data/hpi/NCSTHPI.csv', names=['date', 'sthpi'], header=0)
hpi_SC = pd.read_csv('../data/hpi/SCSTHPI.csv', names=['date', 'sthpi'], header=0)
hpi_VA = pd.read_csv('../data/hpi/VASTHPI.csv', names=['date', 'sthpi'], header=0)

hpi_AL['state'] = 'AL'
hpi_GA['state'] = 'GA'
hpi_MN['state'] = 'MN'
hpi_NC['state'] = 'NC'
hpi_SC['state'] = 'SC'
hpi_VA['state'] = 'VA'

hpi_AL['year'] = pd.DatetimeIndex(hpi_AL.date).year
hpi_GA['year'] = pd.DatetimeIndex(hpi_GA.date).year
hpi_MN['year'] = pd.DatetimeIndex(hpi_MN.date).year
hpi_NC['year'] = pd.DatetimeIndex(hpi_NC.date).year
hpi_SC['year'] = pd.DatetimeIndex(hpi_SC.date).year
hpi_VA['year'] = pd.DatetimeIndex(hpi_VA.date).year

hpi = pd.concat([hpi_AL, hpi_GA, hpi_MN, hpi_NC, hpi_SC, hpi_VA], ignore_index=True)

# Filter data by years
hpi = hpi[(hpi.year >= 1990) & (hpi.year <= 2006)]

# Extract aggregate stats
hpi = hpi.groupby(['year', 'state'])['sthpi'].mean().reset_index()

# Income data management
income_AL = pd.read_csv('../data/median_household_income/MEHOINUSALA646N.csv',
                        names=['date', 'mh_income'], header=0)
income_GA = pd.read_csv('../data/median_household_income/MEHOINUSGAA646N.csv',
                        names=['date', 'mh_income'], header=0)
income_MN = pd.read_csv('../data/median_household_income/MEHOINUSMNA646N.csv',
                        names=['date', 'mh_income'], header=0)
income_NC = pd.read_csv('../data/median_household_income/MEHOINUSNCA646N.csv',
                        names=['date', 'mh_income'], header=0)
income_SC = pd.read_csv('../data/median_household_income/MEHOINUSSCA646N.csv',
                        names=['date', 'mh_income'], header=0)
income_VA = pd.read_csv('../data/median_household_income/MEHOINUSVAA646N.csv',
                        names=['date', 'mh_income'], header=0)

income_AL['state'] = 'AL'
income_GA['state'] = 'GA'
income_MN['state'] = 'MN'
income_NC['state'] = 'NC'
income_SC['state'] = 'SC'
income_VA['state'] = 'VA'

income_AL['year'] = pd.DatetimeIndex(income_AL.date).year
income_GA['year'] = pd.DatetimeIndex(income_GA.date).year
income_MN['year'] = pd.DatetimeIndex(income_MN.date).year
income_NC['year'] = pd.DatetimeIndex(income_NC.date).year
income_SC['year'] = pd.DatetimeIndex(income_SC.date).year
income_VA['year'] = pd.DatetimeIndex(income_VA.date).year

income = pd.concat([income_AL, income_GA, income_MN, income_NC, income_SC, income_VA],
                   ignore_index=True)

# Filter data by years
income = income[(income.year >= 1990) & (income.year <= 2006)]

# Extract aggregate stats
income = income.groupby(['year', 'state'])['mh_income'].mean().reset_index()

state_data = state_data.rename(columns={'as_of_year': 'year'})
state_data['elapsed_time'] = state_data.year - 1990

state_data['prime'] = state_data.total - state_data.subprime
state_data['prime_originated'] = state_data.loans_originated - state_data.subprime_originated
state_data['prime_amount'] = state_data.loan_amount - state_data.subprime_amount

state_data['state'] = 'AL'
state_data.loc[state_data.state_code == 13, 'state'] = 'GA'
state_data.loc[state_data.state_code == 27, 'state'] = 'MN'
state_data.loc[state_data.state_code == 37, 'state'] = 'NC'
state_data.loc[state_data.state_code == 45, 'state'] = 'SC'
state_data.loc[state_data.state_code == 51, 'state'] = 'VA'

# Merge with population data
state_data = pd.merge(state_data, state_population, how='inner', on=['year', 'state'])

# Merge with hpi data
state_data = pd.merge(state_data, hpi, how='inner', on=['year', 'state'])

# Merge with income data
state_data = pd.merge(state_data, income, how='inner', on=['year', 'state'])

state_data = state_data.fillna(0)

state_relative = state_relative.rename(columns={'as_of_year': 'year'})
state_relative['elapsed_time'] = state_relative.year - 1990

state_relative['prime'] = 1 - state_relative.subprime
state_relative['prime_originated'] = state_relative.loans_originated - state_relative.subprime_originated
state_relative['prime_amount'] = state_data.prime_amount / state_data.prime

state_relative['state'] = 'AL'
state_relative.loc[state_relative.state_code == 13, 'state'] = 'GA'
state_relative.loc[state_relative.state_code == 27, 'state'] = 'MN'
state_relative.loc[state_relative.state_code == 37, 'state'] = 'NC'
state_relative.loc[state_relative.state_code == 45, 'state'] = 'SC'
state_relative.loc[state_relative.state_code == 51, 'state'] = 'VA'

# Merge with population data
state_relative = pd.merge(state_relative, state_population, how='inner', on=['year', 'state'])

# Merge with hpi data
state_relative = pd.merge(state_relative, hpi, how='inner', on=['year', 'state'])

# Merge with income data
state_relative = pd.merge(state_relative, income, how='inner', on=['year', 'state'])

state_relative = state_relative.fillna(0)

# Add DID dummies
state_relative['did_NC'] = 0
state_relative['did_GA'] = 0
state_relative['did_MN'] = 0
state_relative['did_SC'] = 0


county_data = county_data.rename(columns={'as_of_year': 'year'})
county_data['elapsed_time'] = county_data.year - 1990

county_data['prime'] = county_data.total - county_data.subprime
county_data['prime_originated'] = county_data.loans_originated - county_data.subprime_originated
county_data['prime_amount'] = county_data.loan_amount - county_data.subprime_amount

county_data['state'] = 'AL'
county_data.loc[county_data.state_code == 13, 'state'] = 'GA'
county_data.loc[county_data.state_code == 27, 'state'] = 'MN'
county_data.loc[county_data.state_code == 37, 'state'] = 'NC'
county_data.loc[county_data.state_code == 45, 'state'] = 'SC'
county_data.loc[county_data.state_code == 51, 'state'] = 'VA'

# Merge with population data
county_data = pd.merge(county_data, state_population, how='inner', on=['year', 'state'])

# Merge with hpi data
county_data = pd.merge(county_data, hpi, how='inner', on=['year', 'state'])

# Merge with income data
county_data = pd.merge(county_data, income, how='inner', on=['year', 'state'])

#county_data = county_data.drop(['county_fips'], axis=1)
county_data = county_data.fillna(0)

county_relative = county_relative.rename(columns={'as_of_year': 'year'})
county_relative['elapsed_time'] = county_relative.year - 1990

county_relative['prime'] = 1 - county_relative.subprime
county_relative['prime_originated'] = county_relative.loans_originated - county_relative.subprime_originated
county_relative['prime_amount'] = county_data.prime_amount / county_data.prime

county_relative['state'] = 'AL'
county_relative.loc[county_relative.state_code == 13, 'state'] = 'GA'
county_relative.loc[county_relative.state_code == 27, 'state'] = 'MN'
county_relative.loc[county_relative.state_code == 37, 'state'] = 'NC'
county_relative.loc[county_relative.state_code == 45, 'state'] = 'SC'
county_relative.loc[county_relative.state_code == 51, 'state'] = 'VA'

# Merge with population data
county_relative = pd.merge(county_relative, state_population, how='inner', on=['year', 'state'])

# Merge with hpi data
county_relative = pd.merge(county_relative, hpi, how='inner', on=['year', 'state'])

# Merge with income data
county_relative = pd.merge(county_relative, income, how='inner', on=['year', 'state'])

#county_relative = county_relative.drop(['county_fips'], axis=1)
county_relative = county_relative.fillna(0)

# Writing final datasets

state_data.to_csv('../data/final/state_data.csv', mode='w')
state_relative.to_csv('../data/final/state_relative.csv', mode='w')
county_data.to_csv('../data/final/county_data.csv', mode='w')
county_relative.to_csv('../data/final/county_relative.csv', mode='w')
