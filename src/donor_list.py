#!/usr/bin/env python3

import os
import math
import glob


class CSVHandler:

    def getAllCSVFiles():
        path = os.getcwd()
        print(path)
        return glob.glob(os.path.join(path, "*.csv"))

    def even(x):
        return x % 2 == 0

    def createExclusionList():
        exclusionFilePath = 'rules/special_case_names.txt'
        with open(exclusionFilePath) as exclusionFile:
            exclusions = exclusionFile.readlines()
            exclusions = [line.strip() for line in exclusions]
        return exclusions

    def makeProperCaseWithExclusions(name, exclusions):
        for excName in exclusions:
            if name.upper() == excName.upper():
                return excName
        return name.title()

    def writeToFile(summaryFileName, summaryFilePath, dataByCycle, aggregation_functions):
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
                summaryFile.write(f'{str(cycleYear)} cycle:')
                for index in dataByCycle[cycleYear].index:
                    summaryFile.write(' ' + str(dataByCycle[cycleYear]['committee_name'][index]) + ' $' + str(format(math.floor(dataByCycle[cycleYear]['total_amount'][index]), ',d')) + ';')
                
                summaryFile.write('\n\n')

            summaryFile.close()


