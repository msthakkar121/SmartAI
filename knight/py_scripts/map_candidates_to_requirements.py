import pandas as pd

from uszipcode import Zipcode, SearchEngine

from knight.neighbours import neighbours_of


class MapCandidatesToRequirements:
    def __init__(self):
        pass

    def map_candidates_to_requirements(self, requirements):
        search = SearchEngine(simple_zipcode=True)
        for i in requirements.index:
            print('Requirement %s \n' % requirements['RequirementID'][i])
            zipcodes = requirements['RequirementZIPCode'][i]
            zipcodes = zipcodes.replace(" ", "")
            zipcodes = zipcodes.split(',')

            all_candidates_in_radius = pd.DataFrame()
            for zipcode in zipcodes:
                obj_zipcode = search.by_zipcode(zipcode)

                my_candidates = pd.read_csv('Data/state_wise/' + obj_zipcode.state + '.csv')
                if 'Unnamed: 0' in my_candidates:
                    my_candidates.drop(labels=['Unnamed: 0'], axis=1, inplace=True)

                for neighbour in neighbours_of[obj_zipcode.state]:
                    df = pd.read_csv('Data/state_wise/' + neighbour + '.csv')
                    if 'Unnamed: 0' in df:
                        df.drop(labels=['Unnamed: 0'], axis=1, inplace=True)
                    my_candidates = pd.concat([my_candidates, df])
                # print(zipcode, ': lat ', obj_zipcode.lat, ', lon ', obj_zipcode.lng)
                print(len(my_candidates), ' candidates')
                in_30_miles = search.by_coordinates(obj_zipcode.lat, obj_zipcode.lng, radius=30, returns=50000)
                for index, zipc in enumerate(in_30_miles):
                    in_30_miles[index] = zipc.zipcode
                # print('ZipCodes in 30 miles: ', len(in_30_miles))
                my_candidates = my_candidates[my_candidates.ZIPCode.isin(in_30_miles)]
                print(len(my_candidates), ' candidates in 30 miles of the requirement.\n')
                all_candidates_in_radius = pd.concat([all_candidates_in_radius, my_candidates])
            print('\n%d Total candidates for the requirement.\n\n' % len(all_candidates_in_radius))
        pass
