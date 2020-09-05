__author__ = "Mohit Thakkar"

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
        cleantext = re.sub(cleanre, ' ', str(raw_html))

        # To lower
        cleantext = cleantext.lower()

        # Remove certain characters
        chars = ['\n', '\t', '\r', '&nbsp;', '"', '. ', ', ', ',', ': ', ':', '? ', '?']
        for char in chars:
            cleantext = cleantext.replace(char, ' ')

        cleantext = cleantext.replace('&amp;', 'and')

        # Strip multiple whitspaces to a single one
        cleantext = re.sub(' +', ' ', str(cleantext)).strip()
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
            if re.search(r'\b' + re.escape(skill) + r'\b', str(job_desc)):
                re_skills.append(skill)
            if re.search(r'\b' + re.escape(skill) + r'\b', str(job_desc)):
                re_skills.append(skill)

        for skill in linkedin_skills:
            skill = str(skill).lower()

            if re.search(r'\b' + re.escape(skill) + r'\b', str(job_desc)):
                re_skills.append(skill)

            if re.search(r'\b' + re.escape(skill) + r'\b', str(job_desc)):
                re_skills.append(skill)

        re_skills = list(dict.fromkeys(re_skills))

        return re_skills

    def match_candidate_skills(self, re_skills, candidates):
        # Pick relevant features from candidate data
        candidates = candidates[
            ['candidateid', 'candidatename', 'resumecontent', 'candidateskills', 'zipcode', 'State']]
        candidates['candidateskills'].fillna(' ', inplace=True)

        # This feature is for candidate score in regards to the requirement we are processing
        candidates['PercentageScore'] = ''

        for i in candidates.index:
            # Clean candidates data
            candidates['resumecontent'].loc[i] = self.cleanhtml(candidates['resumecontent'].loc[i])
            candidates['candidateskills'].loc[i] = self.cleanhtml(candidates['candidateskills'].loc[i])
            candidates['PercentageScore'].loc[i] = self.get_percentage_score(re_skills,
                                                                             candidates['resumecontent'].loc[i] + ' ' +
                                                                             candidates['candidateskills'].loc[i])

        return candidates

    def get_percentage_score(self, skills, resume_data):
        percentage_score = 0
        total_skills_count = len(skills)
        matching_skills_count = 0

        for skill in skills:
            skill = str(skill).lower()
            if re.search(r'\b' + re.escape(skill) + r'\b', str(resume_data)):
                matching_skills_count = matching_skills_count + 1

        percentage_score = (matching_skills_count * 100) / total_skills_count
        return percentage_score

    def score_candidates(self, requirement, candidates):
        # Clean job data
        requirement['RequirementJobDescription'] = self.cleanhtml(
            requirement['RequirementJobDescription'])
        requirement['ActualRequirement'] = self.cleanhtml(requirement['ActualRequirement'])
        requirement['JobTitle'] = self.cleanhtml(requirement['JobTitle'])

        # Get a list of skills from job data
        re_skills = self.get_requirement_skills(
            requirement['RequirementJobDescription'] + ' ' + requirement['JobTitle'])

        # Get a list of candidates suitable or this job along with their score,
        # which indicates their relevance to the job
        candidates = self.match_candidate_skills(re_skills, candidates)
        candidates.sort_values(by='PercentageScore', ascending=False, ignore_index=True, inplace=True)

        candidates.to_csv(str(requirement['RequirementID']) + '_candidates.csv')

        print(len(candidates), ' candidates shortlisted...!!!')
        pass
