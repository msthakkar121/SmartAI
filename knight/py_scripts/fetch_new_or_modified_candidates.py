__author__ = "Mohit Thakkar"

import os
import csv
import pandas as pd
from datetime import datetime

from dateutil.relativedelta import relativedelta
from uszipcode import SearchEngine

from knight.db_scripts import logger
from knight.db_scripts.fetch_new_or_modified_candidates import FetchNewOrModifiedCandidates as FNMC

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchNewOrModifiedCandidates:
    def __init__(self):
        import sys
        import csv
        maxInt = sys.maxsize

        while True:
            # decrease the maxInt value by factor 10
            # as long as the OverflowError occurs.

            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt / 10)
        pass

    def fetch_new_or_modified_candidates(self):
        print('\n\nFetching new/updated candidates...')

        # Get the data
        obj = FNMC()
        df = obj.fetch_new_or_modified_candidates()
        df['resumecontent'] = df['resumecontent'].to_string()
        obj.connection.close()

        print('\n\n', df.head(), '\n\nFetched ', len(df), 'candidates from the database.')
        logger.log('(' + str(datetime.now()) + ') Fetched' + str(len(df)) + 'candidates from the database.')

        if len(df) > 0:
            # Add 'States' to candidates
            search = SearchEngine(simple_zipcode=True)
            df['State'] = ''
            for i in df.index:
                df['State'][i] = search.by_zipcode(df['ZIPCode'][i]).state

            # Remove Invalid States
            df = df[df.State.notnull()]

            for state in df.State.unique():
                state_df = pd.read_csv(BASE_DIR + '/ration/data/candidates/state_wise/' + state + '.csv',
                                       engine='python', encoding='utf-8')
                state_df = state_df[state_df.columns.drop(list(state_df.filter(regex='Unnamed:')))]
                state_df['resumecontent'] = state_df['resumecontent'].to_string()
                new_candidates_for_state = df[df['State'] == state]
                new_candidates_for_state.reset_index(drop=True, inplace=True)

                for i, candidate in new_candidates_for_state.iterrows():
                    if candidate['candidateid'] in state_df.candidateid.values:
                        state_df.drop(state_df.loc[state_df['candidateid'] == candidate['candidateid']].index,
                                      inplace=True)
                    state_df = state_df.append(new_candidates_for_state.loc[i], ignore_index=True)

                # Drop candidates older than 1.5 years
                state_df['updateddate'] = pd.to_datetime(state_df['updateddate'])
                state_df = state_df[state_df['updateddate'] > (datetime.now() - relativedelta(months=18))]

                # Drop duplicates
                state_df.drop_duplicates(inplace=True, ignore_index=True)

                # Write new file and close the stream
                file = open(BASE_DIR + '/ration/data/candidates/state_wise/' + state + '.csv', 'wt', encoding="utf-8")
                candidates = csv.writer(file)
                candidates.writerow(state_df.columns.tolist())
                candidates.writerows(state_df.values.tolist())
                file.close()
                # state_df.to_csv(BASE_DIR + '/ration/data/candidates/state_wise/' + state + '.csv', encoding='utf-8')
        return
