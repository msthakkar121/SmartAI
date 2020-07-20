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
        for char in chars:
            cleantext = cleantext.replace(char, ' ')

        cleantext = cleantext.replace('&amp;', 'and')

        # Strip multiple whitspaces to a single one
        cleantext = re.sub(' +', ' ', cleantext).strip()
        return cleantext

    def get_requirement_skills(self, job_desc):
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

        skills = skills['SkillName'].values.tolist()
        linkedin_skills = linkedin_skills['SkillName'].values.tolist()

        re_skills = []

        for skill in skills:
            skill = str(skill).lower()
            if re.search(r'\b' + re.escape(skill) + r'\b', job_desc):
                re_skills.append(skill)
            if re.search(r'\b' + re.escape(skill) + r'\b', job_desc):
                re_skills.append(skill)

        for skill in linkedin_skills:
            skill = str(skill).lower()

            if re.search(r'\b' + re.escape(skill) + r'\b', job_desc):
                re_skills.append(skill)

            if re.search(r'\b' + re.escape(skill) + r'\b', job_desc):
                re_skills.append(skill)

        re_skills = list(dict.fromkeys(re_skills))

        return re_skills

    def match_candidate_skills(self, re_skills, candidates):
        return candidates

    def score_candidates(self, requirement, candidates):

        requirement['RequirementJobDescription'].loc[0] = self.cleanhtml(
            requirement['RequirementJobDescription'].loc[0])
        requirement['ActualRequirement'].loc[0] = self.cleanhtml(requirement['ActualRequirement'].loc[0])
        requirement['JobTitle'].loc[0] = self.cleanhtml(requirement['JobTitle'].loc[0])

        re_skills = self.get_requirement_skills(
            requirement['RequirementJobDescription'].loc[0] + ' ' + requirement['JobTitle'].loc[0])

        candidates = self.match_candidate_skills(re_skills, candidates)

        print('Scoring candidates is work in progress...!!!')
        pass
