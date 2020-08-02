__author__ = "Mohit Thakkar"

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

            # Remove Invalid States
            df = df[df.State.notnull()]

            for state in df.State.unique():
                state_df = pd.read_csv(BASE_DIR + '/ration/data/candidates/state_wise/' + state + '.csv')
                new_candidates_for_state = df[df['State'] == state]
                new_candidates_for_state.reset_index(drop=True, inplace=True)

                for i, candidate in new_candidates_for_state.iterrows():
                    if candidate['CandidateID'] in state_df.CandidateID.values:
                        state_df.drop(state_df.loc[state_df['CandidateID'] == candidate['CandidateID']].index,
                                      inplace=True)
                    state_df = state_df.append(new_candidates_for_state.loc[i], ignore_index=True)

                state_df.to_csv(BASE_DIR + '/ration/data/candidates/state_wise/' + state + '.csv')
        return
