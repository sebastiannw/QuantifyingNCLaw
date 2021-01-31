#import pandas as pd

# Define properties of the datasets
#   Define width of every column in the datasets
ends_population = [4, 6, 8, 11, 13, 14, 15, 16, 18, 26]
ends = {'population': ends_population}

#   Define column names for each column in the datasets
names_population = ['year', 'state', 'state_fips', 'county_fips', 'registry', 'race', 'origin', 'sex', 'age', 'population']
names = {'population': names_population}

int_list = {'population': [9]}

# Loop until a valid file_type is entered
invalid_input = True

while invalid_input:
    try:
        file_type = input('Enter a file type: ')
        if (file_type not in ends.keys()) or (file_type not in names.keys()):
            raise ValueError('Enter a valid file type:')
            for x in ends.keys():
                print(x)
        invalid_input = False
    except:
        print('Enter a valid file type:')
        for x in ends.keys():
            print(x)

# Creates a panda dataframe from raw text file, filling empty cells with 'NA'
#data = pd.read_fwf('../data/hmda/' + file_type + 'short.txt', ends=ends[file_type], header=None, names=names[file_type])
#data = pd.read_fwf('../data/hmda/HMS.U' + file_type + '.LARS', ends=ends[file_type], header=None, names=names[file_type])

# Opens source file and reads line by line
#with open('../data/hmda/' + file_type + 'short.txt', 'r') as file:

input_files = {'population': '../data/population/us.1969_2018.19ages.adjusted.txt'}
input_file = input_files[file_type]

with open(input_file, 'r', encoding='latin-1') as file:
    # Creates output CSV file
    out = open('../data/population/' + file_type + '.csv', 'w')

    # Adds header to output file
    header = ''
    for name in names[file_type]:
        header += name + ','
    header = header[:len(header) - 1]
    out.write(header)
    out.write('\n')
    print('Processing...')

    # Read each line of source file in loop
    for line in file:
        line = line.strip()
        # Creates output string
        out_line = ''

        # Iterates over columns in HMDA LAR data
        for i in range(len(ends[file_type])):
            if i == 0:
                value = line[:ends[file_type][i]]
            else:
                # Strips unnecessary spaces
                value = line[ends[file_type][i - 1]:ends[file_type][i]].strip()
                # Inputs 'NA' if value is empty
                value = 'NA' if value == '' else value
                # Converts to int if it's a number
                if i in int_list[file_type]:
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
#data.to_csv('../CSVs/hmda' + file_type + '.csv', index=False)
