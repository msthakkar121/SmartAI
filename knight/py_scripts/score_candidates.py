import os
import re

import pandas as pd

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ScoreCandidates:
    def __init__(self):
        pass

    def cleanhtml(self, raw_html):
        # Remove HTML Tags
        cleanre = re.compile('<.*?>')
        cleantext = re.sub(cleanre, ' ', raw_html)

        # To lower
        cleantext = cleantext.lower()

        # Remove certain characters
        chars = ['\n', '\t', '. ', ', ', ',', ': ', ':', '? ', '?']
        for c in chars:
            cleantext = cleantext.replace(c, ' ')

        # Strip multiple whitspaces to a single one
        cleantext = re.sub(' +', ' ', cleantext).strip()
        return cleantext

    def score_candidates(self, requirement, candidates):
        # Get SourcePros Skills
        skills = pd.read_csv(BASE_DIR + '/ration/data/skills.csv')

        if 'Unnamed: 0' in skills:
            skills.drop(labels=['Unnamed: 0'], axis=1, inplace=True)

        skills['SkillName'] = skills['SkillName'].str.replace('"', '')
        skills['SkillName'] = skills['SkillName'].str.replace(' ', '')

        # Get LinkedIn Skills
        linkedin_skills = pd.read_csv(BASE_DIR + '/ration/data/linkedin_skills', header=0, names=['SkillName'])
        if 'Unnamed: 0' in linkedin_skills:
            linkedin_skills.drop(labels=['Unnamed: 0'], axis=1, inplace=True)

        requirement['RequirementJobDescription'].loc[0] = self.cleanhtml(requirement['RequirementJobDescription'].loc[0])
        requirement['ActualRequirement'].loc[0] = self.cleanhtml(requirement['ActualRequirement'].loc[0])
        requirement['JobTitle'].loc[0] = self.cleanhtml(requirement['JobTitle'].loc[0])

        print('Scoring candidates is work in progress...!!!')
        pass
