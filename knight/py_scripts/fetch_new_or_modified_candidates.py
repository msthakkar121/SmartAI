import os
import pandas as pd

from uszipcode import SearchEngine

from knight.db_scripts.fetch_new_or_modified_candidates import FetchNewOrModifiedCandidates as FNMC

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchNewOrModifiedCandidates:
    def __init__(self):
        pass

    def fetch_new_or_modified_candidates(self):
        print('\n\nFetching new/updated candidates...')

        # Get the data
        obj = FNMC()
        df = obj.fetch_new_or_modified_candidates()
        print('\n\n', df.head(), '\n\nFetched ', len(df), 'candidates from the database.')

        if len(df) > 0:
            # Add 'States' to candidates
            search = SearchEngine(simple_zipcode=True)
            df['State'] = ''
            for i in df.index:
                df['State'][i] = search.by_zipcode(df['ZIPCode'][i]).state

            for state in df.State.unique():
                state_df = pd.read_csv(BASE_DIR + '/ration/data/candidates/state_wise/' + state + '.csv')
                new_candidates_for_state = df[df['State'] == state]

                # TODO

                state_df.to_csv(BASE_DIR + '/ration/data/candidates/state_wise/' + state + '.csv')
        return
