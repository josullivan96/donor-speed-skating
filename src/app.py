import pandas as pd
import collections

from donor_list import CSVHandler


# =============================================================================
allFiles = CSVHandler.getAllCSVFiles()
for file in allFiles:
    # handle file importing and file names
    fileName = file

     # read in csv and strip unnecessary columns
    rawDataframe = pd.read_csv(fileName)
    data = rawDataframe[['committee_name', 'report_year', 'contribution_receipt_amount', 'contributor_first_name', 'contributor_last_name']]

    # create summary fileName with donor name
    # ADD TO different file
    donorNameString = str(data['contributor_last_name'][0]).upper() + '_' + str(data['contributor_first_name'][0]).upper()
    summaryFileName = f'{donorNameString}_summary.txt'
    summaryFilePath = f'./{summaryFileName}'

    # create exclusion list 
    exclusionList = CSVHandler.createExclusionList()

    # make names proper case taking into consideration exclusions
    for index in data.index:
        updatedName = CSVHandler.makeProperCaseWithExclusions(data['committee_name'][index], exclusionList)
        data.at[index, 'committee_name'] = updatedName

    # get array of election cycles (include even year and previous year)
    electionCycles = list(filter(CSVHandler.even, data['report_year'].unique()))
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
    # ADD TO CONSTANTS
    aggregation_functions = {'report_year': 'first', 'contribution_receipt_amount': 'sum'}

    CSVHandler.writeToFile(summaryFileName, summaryFilePath, dataByCycle, aggregation_functions)
