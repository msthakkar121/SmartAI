import os

from knight.db_scripts.fetch_all_candidates import FetchAllCandidates as FAC

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchAllCandidates:
    def __init__(self):
        pass

    def fetch_all_candidates(self):
        # Create the directory to save the data
        data_path = BASE_DIR + '/ration/Data/'
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

        # Save the data
        try:
            df.to_csv(data_path + 'candidates.csv')
        except OSError as ose:
            print('\nError saving data.\n', ose)
        else:
            print('\nSuccessfully saved the data.')
