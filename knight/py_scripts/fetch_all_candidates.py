__author__ = "Mohit Thakkar"

import os
import pandas as pd

from uszipcode import SearchEngine, state_abbr

from knight.db_scripts.fetch_all_candidates import FetchAllCandidates as FAC

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchAllCandidates:
    def __init__(self):
        pass

    def fetch_all_candidates(self):
        # Create the directory to save the data
        data_path = BASE_DIR + '/ration/data/candidates/state_wise'
        try:
            os.makedirs(data_path, exist_ok=True)
        except OSError:
            print('Creation of directory %s failed' % data_path)
        else:
            print('Successfully created the directory %s' % data_path)

        print('\n\nFetching the data...')

        # Get the data
        obj = FAC()
        df = obj.fetch_all_candidates()
        obj.connection.close()

        print('\n\n', df.head(), '\n\nFetched ', len(df), 'candidates from the database.')

        # Divide candidates based on location
        search = SearchEngine(simple_zipcode=True)

        # Add State column in the DataFrame
        df['State'] = ''

        # Set state value for each candidate
        for i in df.index:
            df['State'][i] = search.by_zipcode(df['zipcode'][i]).state

        # Dictionary of dataframes, one for each state
        dict_states_dframes = {}
        for state in state_abbr.STATE_ABBR_SHORT_TO_LONG:
            dict_states_dframes[state] = pd.DataFrame(columns=df.columns)
            dict_states_dframes[state] = df[df['State'] == state]
            dict_states_dframes[state].reset_index(inplace=True, drop=True)
            try:
                dict_states_dframes[state].to_pickle(data_path + '/' + state + '.pkl', protocol=0)
            except OSError as ose:
                print('\nError saving data.\n', ose)
            except Exception as e:
                print('\nError saving data.\n', e)
            else:
                print('\nSuccessfully saved the data for %s location.' % state)
