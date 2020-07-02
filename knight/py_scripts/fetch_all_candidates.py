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
        data_path = BASE_DIR + '/ration/Data/state_wise'
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

        print('\n\n', df.head(), '\n\nFetched ', len(df), 'candidates from the database.')

        # Divide candidates based on location
        search = SearchEngine(simple_zipcode=True)
        df['State'] = ''
        for i in df.index:
            df['state'][i] = search.by_zipcode(df['ZIPCode'][i]).state

        # Dictionary of dataframes, one for each state
        dict_states_dframes = {}
        for state in state_abbr.STATE_ABBR_SHORT_TO_LONG:
            dict_states_dframes[state] = pd.DataFrame(columns=df.columns)
            dict_states_dframes[state] = df[df['state'] == state]
            try:
                dict_states_dframes[state].to_csv(data_path + state + '.csv')
            except OSError as ose:
                print('\nError saving data.\n', ose)
            except Exception as e:
                print('\nError saving data.\n', e)
            else:
                print('\nSuccessfully saved the data for %s location.' % state)
