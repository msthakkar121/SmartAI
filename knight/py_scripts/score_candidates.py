__author__ = "Mohit Thakkar"

import gc
import os
import re
from datetime import datetime

import pandas as pd

from knight.db_scripts import logger

from knight.db_scripts.email_candidates import EmailCandidates

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

        skills = skills[skills.columns.drop(list(skills.filter(regex='Unnamed:')))]

        skills['SkillName'] = skills['SkillName'].str.replace('"', '')
        skills['SkillName'] = skills['SkillName'].str.replace(' ', '')

        # Get LinkedIn Skills
        linkedin_skills = pd.read_csv(BASE_DIR + '/ration/data/linkedin_skills', header=0, names=['SkillName'])
        linkedin_skills = linkedin_skills[linkedin_skills.columns.drop(list(linkedin_skills.filter(regex='Unnamed:')))]

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

    def get_percentage_score(self, skills, resume_data):
        matching_skills_count = 0

        for skill in skills:
            if re.search(r'\b' + re.escape(str(skill).lower()) + r'\b', str(resume_data)):
                matching_skills_count = matching_skills_count + 1

        return (matching_skills_count * 100) / len(skills)

    def score_candidates(self, requirement, candidates):
        # Clean job data
        requirement.at['RequirementJobDescription'] = self.cleanhtml(
            requirement.get('RequirementJobDescription'))
        requirement.at['ActualRequirement'] = self.cleanhtml(requirement.get('ActualRequirement'))
        requirement.at['JobTitle'] = self.cleanhtml(requirement.get('JobTitle'))

        # Get a list of skills from job data
        re_skills = self.get_requirement_skills(
            requirement['RequirementJobDescription'] + ' ' + requirement['JobTitle'])

        # Get a list of candidates suitable or this job along with their score,
        # which indicates their relevance to the job

        # Match candidate skills
        # Pick relevant features from candidate data
        candidates.drop(candidates.columns.difference(
            ['candidateid', 'candidatename', 'resumecontent', 'candidateskills', 'zipcode', 'State']
        ), 1, inplace=True)
        candidates['candidateskills'].fillna(' ', inplace=True)

        # This feature is for candidate score in regards to the requirement we are processing
        candidates.insert(len(candidates.columns), 'PercentageScore', '')
        candidates.reset_index(inplace=True, drop=True)
        for i in candidates.index:
            # Clean candidates data
            # candidates.at[i, 'resumecontent'] = self.cleanhtml(candidates.loc[i, 'resumecontent'])
            candidates.at[i, 'candidateskills'] = self.cleanhtml(candidates.loc[i, 'candidateskills'])
            candidates.at[i, 'PercentageScore'] = self.get_percentage_score(re_skills,
                                                                            candidates.loc[i, 'resumecontent'] + ' ' +
                                                                            candidates.loc[i, 'candidateskills'])

        candidates.drop(candidates[candidates['PercentageScore'] == 0].index, inplace=True)
        candidates.sort_values(by='PercentageScore', ascending=False, ignore_index=True, inplace=True)

        # Get candidates with score greater than 40%
        candidates_to_email = candidates[candidates['PercentageScore'] > 40]

        # In case there are less than 50 candidates with score greater than 40%,
        # then email top 50 candidates shortlisted regardless of their score
        if len(candidates_to_email) < 50:
            candidates_to_email = candidates.head(50)

        # In case there are more than 100 candidates with score greater than 40%,
        # then email top 100 candidates shortlisted based on their score
        if len(candidates_to_email) > 100:
            candidates_to_email.sort_values(by='PercentageScore', ascending=False, ignore_index=True, inplace=True)
            candidates_to_email = candidates_to_email.head(100)

        number_of_candidates = len(candidates_to_email)

        # Store all candidates
        # candidates.to_csv(str(requirement['RequirementID']) + '_candidates.csv')

        # Normalize scores in the range of 80% to 100%
        candidates_to_email['PercentageScore'] = [(float(i) * 20 / max(candidates_to_email['PercentageScore'])) + 80 for
                                                  i in candidates_to_email['PercentageScore']]

        # Generate comma separated values for candidates & scores
        csv_candidate_ids = ",".join([str(score) for score in candidates_to_email['candidateid'].values])
        csv_scores = ",".join([str(score) for score in candidates_to_email['PercentageScore'].values])

        # Send email
        obj = EmailCandidates()
        obj.email_candidates(requirement['RequirementID'], csv_candidate_ids, csv_scores)

        logger.log('(' + str(datetime.now()) + ') Shortlisted ' + str(
            number_of_candidates) + 'candidates for requirement ' + requirement['RequirementID'] + '.')

        print(number_of_candidates, ' candidates shortlisted...!!!')
        pass
