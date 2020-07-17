#import pandas as pd

# Define properties of the HMDA LAR datasets for each year
#   Define width of every column in the datasets
#widths_1 = [4, 10, 1, 1, 1, 1, 5, 1, 4, 2, 3, 7, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 7]
#widths_2 = [4, 10, 1, 1, 1, 1, 5, 1, 5, 2, 3, 7, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 7]
widths_0 = [28, 36, 40, 46, 48, 51, 52, 54, 55, 59, 68, 69, 73, 82, 83, 87, 96, 97, 101, 110, 111, 115, 124, 125, 126]
widths_1 = [4, 14, 15, 16, 17, 18, 23, 24, 28, 30, 33, 40, 41, 42, 43, 44, 48, 49, 50, 51, 52, 53, 60]
widths_2 = [4, 14, 15, 16, 17, 18, 23, 24, 29, 31, 34, 41, 42, 43, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 71, 72, 73, 80]

widths = {'1981': widths_0, '1982': widths_0, '1983': widths_0, '1984': widths_0,
          '1985': widths_0, '1986': widths_0, '1987': widths_0, '1988': widths_0, '1989': widths_0,
          '1990': widths_1, '1991': widths_1, '1992': widths_1, '1993': widths_1, '1994': widths_1,
          '1995': widths_1, '1996': widths_1, '1997': widths_1, '1998': widths_1, '1999': widths_1,
          '2000': widths_1, '2001': widths_1, '2002': widths_1, '2003': widths_1, '2004': widths_2,
          '2005': widths_2, '2006': widths_2, '2007': widths_2, '2008': widths_2, '2009': widths_2}

#   Define column names for each column in the datasets
names_0 = ['respondent_name', 'respondent_id', 'msamd', 'census_tract_number', 'state_code',
           'county_code', 'agency_code', 'census_validity_flag', 'va_validity_flag', 'va_number_of_loans',
           'va_total_amount', 'conv_validity_flag', 'conv_number_of_loans', 'conv_total_amount', 'hi_validity_flag',
           'hi_number_of_loans', 'hi_total_amount', 'amf_validity_flag', 'amf_number_of_loans', 'amf_total_amount',
           'nol_validity_flag', 'nol_number_of_loans', 'nol_total_amount', 'record_quality_flag', 'filler']
names_1 = ['as_of_year', 'respondent_id', 'agency_code', 'loan_type', 'loan_purpose',
           'owner_occupancy', 'loan_amount', 'action_taken', 'msamd', 'state_code',
           'county_code', 'census_tract_number', 'applicant_race', 'co_applicant_race', 'applicant_sex',
           'co_applicant_sex', 'applicant_income', 'purchaser_type', 'denial_reason_1', 'denial_reason_2',
           'denial_reason_3', 'edit_status', 'sequence_number']
names_2 = ['as_of_year', 'respondent_id', 'agency_code', 'loan_type', 'loan_purpose',
           'owner_occupancy', 'loan_amount', 'action_taken', 'msamd', 'state_code',
           'county_code', 'census_tract_number', 'applicant_sex', 'co_applicant_sex', 'applicant_income',
           'purchaser_type', 'denial_reason_1', 'denial_reason_2', 'denial_reason_3', 'edit_status',
           'property_type', 'preapprovals', 'applicant_ethnicity', 'co_applicant_ethnicity', 'applicant_race_1',
           'applicant_race_2', 'applicant_race_3', 'applicant_race_4', 'applicant_race_5', 'co_applicant_race_1',
           'co_applicant_race_2', 'co_applicant_race_3', 'co_applicant_race_4', 'co_applicant_race_5', 'rate_spread',
           'hoepa_status', 'lien_status', 'sequence_number']

names = {'1981': names_0, '1982': names_0, '1983': names_0, '1984': names_0,
         '1985': names_0, '1986': names_0, '1987': names_0, '1988': names_0, '1989': names_0,
         '1990': names_1, '1991': names_1, '1992': names_1, '1993': names_1, '1994': names_1,
         '1995': names_1, '1996': names_1, '1997': names_1, '1998': names_1, '1999': names_1,
         '2000': names_1, '2001': names_1, '2002': names_1, '2003': names_1, '2004': names_2,
         '2005': names_2, '2006': names_2, '2007': names_2, '2008': names_2, '2009': names_2}

list_0 = [9, 10, 12, 13, 15, 16, 18, 19, 21, 22]
list_1 = [5, 6, 16]
list_2 = [5, 6, 14, 34]

int_list = {'1981': list_0, '1982': list_0, '1983': list_0, '1984': list_0,
            '1985': list_0, '1986': list_0, '1987': list_0, '1988': list_0, '1989': list_0,
            '1990': list_1, '1991': list_1, '1992': list_1, '1993': list_1, '1994': list_1,
            '1995': list_1, '1996': list_1, '1997': list_1, '1998': list_1, '1999': list_1,
            '2000': list_1, '2001': list_1, '2002': list_1, '2003': list_1, '2004': list_2,
            '2005': list_2, '2006': list_2, '2007': list_2, '2008': list_2, '2009': list_2}

# Loop until a valid year is entered
invalid_input = True

while invalid_input:
    try:
        year = input('Enter a 4-digit year: ')
        if (year not in widths.keys()) or (year not in names.keys()):
            raise ValueError('Enter a valid 4-digit year from 1981 to 2009.')
        invalid_input = False
    except:
        print('Enter a valid 4-digit year from 1981 to 2009.')

# Creates a panda dataframe from raw text file, filling empty cells with 'NA'
#data = pd.read_fwf('../RawData/' + year + 'short.txt', widths=widths[year], header=None, names=names[year])
#data = pd.read_fwf('../RawData/HMS.U' + year + '.LARS', widths=widths[year], header=None, names=names[year])

# Opens source file and reads line by line
#with open('../RawData/' + year + 'short.txt', 'r') as file:

input_file = 'HMS.U' + year + '.LARS'
if int(year) < 1990:
    input_file = 'HMD_FACDSB' + year[2:] + '.txt'

with open(input_file, 'r', encoding='latin-1') as file:
    # Creates output CSV file
    out = open('hmda' + year + '.csv', 'w')

    # Adds header to output file
    header = ''
    for name in names[year]:
        header += name + ','
    header = header[:len(header) - 1]
    out.write(header)
    out.write('\n')
    print('Writing file...')

    # Read each line of source file in loop
    for line in file:
        line = line.strip()
        # Creates output string
        out_line = ''

        # Iterates over columns in HMDA LAR data
        for i in range(len(widths[year])):
            if i == 0:
                value = line[:widths[year][i]].strip().replace(',', ';')
            else:
                # Strips unnecessary spaces
                value = line[widths[year][i - 1]:widths[year][i]].strip().replace(',', ';')
                # Inputs 'NA' if value is empty
                value = 'NA' if value == '' else value
                # Converts to int if it's a number
                if i in int_list[year]:
                    try:
                        value = int(value)
                        value = str(value)
                    except:
                        pass
                # Adds comma to create CSV file
                value = ',' + value
            out_line += value
        # write line to output file
        out.write(out_line)
        out.write('\n')
    out.close()

print('DONE!')
#data = data.fillna('NA')

# Writes CSV file
#data.to_csv('../CSVs/hmda' + year + '.csv', index=False)
