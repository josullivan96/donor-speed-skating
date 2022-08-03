import pandas as pd

# FUNCTIONS ===================================================================

def even(x):
    return x % 2 == 0

# =============================================================================

# handle file importing
fileName = 'robert_dyson.csv'

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

# aggregation config
aggregation_functions = {'report_year': 'first', 'contribution_receipt_amount': 'sum'}

# open txt file to write to

with open(fileName.split('.')[0] + '_summary.txt', 'w') as summaryFile:
    # combine donation amounts for same recepient within an election cycle
    for cycleYear in dataByCycle.keys():
        dataByCycle[cycleYear] = dataByCycle[cycleYear].groupby(dataByCycle[cycleYear]['committee_name']).aggregate(aggregation_functions)
        dataByCycle[cycleYear].rename(columns={"contribution_receipt_amount": "total_amount"}, inplace=True)
        # sort by amount descending
        dataByCycle[cycleYear].sort_values(by=['total_amount'], ascending=False, inplace=True)
    #     f.write('readme')


print(dataByCycle[2020])
print(type(dataByCycle[2020]))


# print(electionCycles)
# print(data)

