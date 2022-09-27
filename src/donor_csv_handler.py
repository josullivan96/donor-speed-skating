#!/usr/bin/env python3

import os
import math
import glob


class DonorCSVHandler:

    def get_all_csv_files():
        path = os.getcwd()
        print(path)
        return glob.glob(os.path.join(path, "*.csv"))

    def even(x):
        return x % 2 == 0

    def create_exclusion_list():
        exclusion_file_list = 'rules/special_case_names.txt'
        with open(exclusion_file_list) as exclusion_file:
            exclusions = exclusion_file.readlines()
            exclusions = [line.strip() for line in exclusions]
        return exclusions

    def make_proper_case_with_exclusions(name, exclusions):
        for exc_name in exclusions:
            if name.upper() == exc_name.upper():
                return exc_name
        return name.title()

    def write_to_file(summary_file_name, summary_file_path, data_by_cycle, aggregation_functions):
        # open txt file to write to
        if os.path.exists(summary_file_path): # delete file if exists
            os.remove(summary_file_path)
        with open(summary_file_name, 'w') as summaryFile:
            for cycle_year in data_by_cycle.keys():
                # aggregate amounts of same recipient
                data_by_cycle[cycle_year] = data_by_cycle[cycle_year].groupby(data_by_cycle[cycle_year]['committee_name'], as_index=False).aggregate(aggregation_functions)
                data_by_cycle[cycle_year].rename(columns={"contribution_receipt_amount": "total_amount"}, inplace=True)

                # sort by amount descending
                data_by_cycle[cycle_year].sort_values(by=['total_amount'], ascending=False, inplace=True)        

                # write to file
                summaryFile.write(f'{str(cycle_year)} cycle:')
                for index in data_by_cycle[cycle_year].index:
                    summaryFile.write(' ' + str(data_by_cycle[cycle_year]['committee_name'][index]) + ' $' + str(format(math.floor(data_by_cycle[cycle_year]['total_amount'][index]), ',d')) + ';')
                
                summaryFile.write('\n\n')

            summaryFile.close()


