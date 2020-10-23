__author__ = "Mohit Thakkar"

import gc
import os

import pandas as pd
from uszipcode import SearchEngine
from datetime import datetime

from knight.db_scripts import logger
from knight.py_scripts.score_candidates import ScoreCandidates

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MapCandidatesToRequirements:
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

    def map_candidates_to_requirements(self, requirements):
        search = SearchEngine(simple_zipcode=True)
        # Drop remote location jobs
        requirements.drop(requirements[requirements['IsRemoteLocation'] == 1].index, inplace=True)
        for i in requirements.index:
            print('Requirement %s \n' % requirements['RequirementID'][i])
            logger.log('(' + str(datetime.now()) + ') Processing requirement: ' + str(
                requirements['RequirementID'][i]) + '.')
            zipcodes = str(requirements['RequirementZIPCode'][i])
            zipcodes = zipcodes.replace(" ", "")
            zipcodes = zipcodes.split(',')

            all_candidates_in_radius = pd.DataFrame()
            for zipcode in zipcodes:
                obj_zipcode = search.by_zipcode(zipcode)
                if not obj_zipcode.lat or not obj_zipcode.lng:
                    break
                in_30_miles = search.by_coordinates(obj_zipcode.lat, obj_zipcode.lng, radius=30, returns=50000)

                my_candidates = pd.DataFrame()
                for neighbour in set([i.state for i in in_30_miles]):
                    df = pd.read_pickle(BASE_DIR + '/ration/data/candidates/state_wise/' + neighbour + '.pkl')
                    df.drop(columns=list(df.filter(regex='Unnamed:')), inplace=True)
                    my_candidates = pd.concat([my_candidates, df])
                    del [[df]]
                    gc.collect()
                # print(zipcode, ': lat ', obj_zipcode.lat, ', lon ', obj_zipcode.lng)
                print(len(my_candidates), ' candidates')

                for index, zipc in enumerate(in_30_miles):
                    in_30_miles[index] = zipc.zipcode
                # print('ZipCodes in 30 miles: ', len(in_30_miles))
                my_candidates = my_candidates[my_candidates.zipcode.isin(in_30_miles)]
                print(len(my_candidates), ' candidates in 30 miles of the requirement.\n')
                all_candidates_in_radius = pd.concat(
                    [all_candidates_in_radius, my_candidates]).drop_duplicates().reset_index(drop=True)
                del [[my_candidates]]
                gc.collect()
            print('\n%d Total candidates for the requirement.\n\n' % len(all_candidates_in_radius))
            if len(all_candidates_in_radius) > 0:
                scoring = ScoreCandidates()
                scoring.score_candidates(requirements.loc[i], all_candidates_in_radius)
            del [[all_candidates_in_radius]]
            gc.collect()
        del [[requirements]]
        gc.collect()
        pass
