import pandas as pd
import collections

from donor_csv_handler import DonorCSVHandler

def handle_single_file(file):
    # handle file importing and file names
    file_name = file

    # read in csv and strip unnecessary columns
    raw_dataframe = pd.read_csv(file_name)
    data = raw_dataframe[['committee_name', 'report_year', 'contribution_receipt_amount', 'contributor_first_name', 'contributor_last_name']]

    # create summary file_name with donor name
    # ADD TO different file
    donor_name_string = str(data['contributor_last_name'][0]).upper() + '_' + str(data['contributor_first_name'][0]).upper()
    summary_file_name = f'{donor_name_string}_summary.txt'
    summary_file_path = f'./{summary_file_name}'

    # reformat and aggregate data
    data_by_cycle = aggregate_data(data)

    # aggregation config
    # ADD TO CONSTANTS
    aggregation_functions = {'report_year': 'first', 'contribution_receipt_amount': 'sum'}

    DonorCSVHandler.write_to_file(summary_file_name, summary_file_path, data_by_cycle, aggregation_functions)

def handle_multiple_files(all_files):
    for file in all_files:
        handle_single_file(file)

def data_update_case(data):
    # create exclusion list 
    exclusion_list = DonorCSVHandler.create_exclusion_list()

    # make names proper case taking into consideration exclusions
    for index in data.index:
        updated_name = DonorCSVHandler.make_proper_case_with_exclusions(data['committee_name'][index], exclusion_list)
        data.at[index, 'committee_name'] = updated_name


def aggregate_data(data):
    # make names of recepients proper case - take into account exceptions list
    data_update_case(data)

    # create array of election cycles (include even year and previous year)
    election_cycles = list(filter(DonorCSVHandler.even, data['report_year'].unique()))
    election_cycles.sort(reverse=False)

    # temp all_years
    all_years = []
    for year in election_cycles:
        all_years.append(year - 1)
        all_years.append(year)

    # dictionary for dataframe per year
    data_by_year = {year : pd.DataFrame() for year in all_years}
    for key in data_by_year.keys():
        data_by_year[key] = data[:][data['report_year'] == key]

    # concatenate yearly data by cycle
    data_by_cycle = {year : pd.DataFrame() for year in election_cycles}
    for year in election_cycles:
        curr_election_cycle_dataframes = [data_by_year[year - 1], data_by_year[year]]
        data_by_cycle[year] = pd.concat(curr_election_cycle_dataframes)

    # sort in descending order by year
    data_by_cycle = collections.OrderedDict(sorted(data_by_cycle.items(), reverse=True))

    return data_by_cycle

def get_all_files():
    return DonorCSVHandler.get_all_csv_files()

def main():
    all_files = get_all_files()
    handle_multiple_files(all_files)

if __name__=="__main__":
    main()