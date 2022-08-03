import pandas as pd
import os
import collections
import math


# FUNCTIONS ===================================================================

def even(x):
    return x % 2 == 0

# =============================================================================

# handle file importing and file names
fileName = 'robert_dyson.csv'
donorNameString = fileName.split('.')[0]
summaryFileName = f'{donorNameString}_summary.txt'
summaryFilePath = f'./{summaryFileName}'

# read in csv and strip unnecessary columns
rawDataframe = pd.read_csv(fileName)
data = rawDataframe[['committee_name', 'report_year', 'contribution_receipt_amount']]

# get array of election cycles (include even year and previous year)
electionCycles = list(filter(even, data['report_year'].unique()))
electionCycles.sort(reverse=False)

# temp allYears
allYears = []
for year in electionCycles:
    allYears.append(year - 1)
    allYears.append(year)

# dictionary for dataframe per year
dataByYear = {year : pd.DataFrame() for year in allYears}
for key in dataByYear.keys():
    dataByYear[key] = data[:][data['report_year'] == key]

# concatenate yearly data by cycle
dataByCycle = {year : pd.DataFrame() for year in electionCycles}
for year in electionCycles:
    currElectionCycleDFs = [dataByYear[year - 1], dataByYear[year]]
    dataByCycle[year] = pd.concat(currElectionCycleDFs)

# sort in descending order by year
dataByCycle = collections.OrderedDict(sorted(dataByCycle.items(), reverse=True))

# aggregation config
aggregation_functions = {'report_year': 'first', 'contribution_receipt_amount': 'sum'}

# open txt file to write to
if os.path.exists(summaryFilePath): # delete file if exists
    os.remove(summaryFilePath)
with open(summaryFileName, 'w') as summaryFile:
    for cycleYear in dataByCycle.keys():
        # aggregate amounts of same recipient
        dataByCycle[cycleYear] = dataByCycle[cycleYear].groupby(dataByCycle[cycleYear]['committee_name'], as_index=False).aggregate(aggregation_functions)
        dataByCycle[cycleYear].rename(columns={"contribution_receipt_amount": "total_amount"}, inplace=True)

        # sort by amount descending
        dataByCycle[cycleYear].sort_values(by=['total_amount'], ascending=False, inplace=True)

        # write to file
        summaryFile.write(f'* {str(cycleYear)} --')
        for index in dataByCycle[cycleYear].index:
            summaryFile.write(' ' + str(dataByCycle[cycleYear]['committee_name'][index]) + ' $' + str(format(math.floor(dataByCycle[cycleYear]['total_amount'][index]), ',d')) + ';')
        
        summaryFile.write('\n\n')

    summaryFile.close()

