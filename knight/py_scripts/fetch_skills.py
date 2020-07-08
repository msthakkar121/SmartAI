import os
import pandas as pd

from knight.db_scripts.fetch_skills import FetchSkills as FS

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchSkills:
    def __init__(self):
        pass

    def fetch_skills(self):
        # Create the directory to save the data
        data_path = BASE_DIR + '/ration/data/'
        try:
            os.makedirs(data_path, exist_ok=True)
        except OSError:
            print('Creation of directory %s failed' % data_path)
        else:
            print('Successfully created the directory %s' % data_path)

        print('\n\nFetching the data...')

        # Get the data
        obj = FS()
        df = obj.fetch_skills()

        try:
            df.to_csv(data_path + '/skills.csv')
        except OSError as ose:
            print('\nError saving data.\n', ose)
        except Exception as e:
            print('\nError saving data.\n', e)
        else:
            print('\nSuccessfully saved the data.')
