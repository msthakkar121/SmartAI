__author__ = "Mohit Thakkar"

import os

import pyodbc
from django.conf import settings

import pandas as pd

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchAllCandidates:
    def __init__(self):
        self.connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                         SERVER=settings.DB_SERVER,
                                         DATABASE=settings.DB_NAME,
                                         UID=settings.DB_USER,
                                         PWD=settings.DB_PASSWORD)

    def fetch_all_candidates(self):
        query = """
                SELECT TOP 1000 
                    cm.CandidateID, 
                    cp.PortalName AS Source,
                    reverse(stuff(reverse(CONCAT(
                        CASE
                        WHEN cm.Prefix IS NULL
                            THEN ''
                            ELSE cm.Prefix + ' '
                        END,
                        CASE
                        WHEN cm.FirstName IS NULL
                            THEN ''
                            ELSE cm.FirstName + ' '
                        END,
                        CASE
                        WHEN cm.MiddleName IS NULL
                            THEN ''
                            ELSE cm.MiddleName + ' '
                        END,
                        CASE
                        WHEN cm.LastName IS NULL
                            THEN ''
                            ELSE cm.LastName + ' '
                        END)), 1, 1, '')) as CandidateName,
                    cm.Email,
                    cm.VerifiedByEmail AS isEmailVerified,
                    cm.Mobile,
                    cm.Birthdate,
                    ed.TotalYears AS TotalExperience,
                    ed.USExperience,
                    cr.ResumeContent,
                    jspm.JobSearchPriorityText AS JobSearchStatus,
                    red.DegreeName AS HighestDegree,
                    red.PassingYear,
                    red.IsGraduate,	
                    vcs.CandidateSkills,
                    zm.ZIPCode,
                    CASE
                        WHEN cm.Relocation IS NULL
                            THEN 0
                            ELSE cm.Relocation
                    END AS willRelocate,
                    CASE
                        WHEN cm.SSN IS NOT NULL
                            THEN 1
                            ELSE 0
                    END AS isSSNAvailable,
                    vm.VisaName AS VisaStatus,
                    cv.VisaExpiryDate,
                    cm.CreatedDate,
                    cm.ModifiedDate AS UpdatedDate
                FROM 
                    dbo.CandidateMaster cm WITH (NOLOCK)
                LEFT JOIN
                    dbo.CandidateContactTxn cct WITH (NOLOCK) ON cm.CandidateID = cct.CandidateID
                LEFT JOIN 
                    dbo.AddressMaster am WITH (NOLOCK) ON cct.AddressID = am.AddressID
                LEFT JOIN
                    dbo.ZIPCodeMaster zm WITH (NOLOCK) ON am.ZIPCodeID = zm.ZIPCodeID
                LEFT JOIN
                    dbo.CandidatePortal cp WITH (NOLOCK) ON cm.CandidateID = cp.CandidateID
                LEFT JOIN
                    dbo.CandidateVisa cv WITH (NOLOCK) ON cm.CandidateID = cv.CandidateID
                LEFT JOIN
                    dbo.VisaMaster vm WITH (NOLOCK) ON cv.VisaID = vm.VisaID
                LEFT JOIN
                    dbo.CandidateResume cr WITH (NOLOCK) ON cm.CandidateID = cr.CandidateID
                LEFT JOIN
                    dbo.ResumeExperiences re WITH (NOLOCK) ON cr.ResumeID = re.ResumeID
                LEFT JOIN
                    dbo.ExperienceDetail ed WITH (NOLOCK) ON re.ExperiencesID = ed.ExperiencesID
                LEFT JOIN
                    dbo.ExperienceJobTitle ejt WITH (NOLOCK) ON ed.ExperienceDetailID = ejt.ExperienceDetailID 
                LEFT JOIN
                    dbo.DisplayCandidateResume dcr WITH (NOLOCK) ON cm.CandidateID = dcr.CandidateID
                LEFT JOIN
                    dbo.CandidateJobSearchPriority cjsp WITH (NOLOCK) ON cm.CandidateID = cjsp.CandidateID
                LEFT JOIN
                    dbo.JobSearchPriorityMaster jspm WITH (NOLOCK) ON cjsp.JobSearchPriorityID = jspm.JobSearchPriorityID
                LEFT JOIN 
                    dbo.ResumeEducation red WITH (NOLOCK) ON cr.ResumeID = red.ResumeID
                LEFT JOIN
                    dbo.vw_CandidateSkills vcs WITH (NOLOCK) ON cm.CandidateID = vcs.CandidateID
                WHERE
                    cm.ModifiedDate > Convert(datetime, '2019-01-01 00:00:00')
                ORDER BY
                    cm.ModifiedDate DESC
        """

        df = pd.read_sql_query(query, self.connection)
        if 'Unnamed: 0' in df:
            df.drop(labels=['Unnamed: 0'], axis=1, inplace=True)
        return df
