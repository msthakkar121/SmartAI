import os

import pyodbc
from django.conf import settings

import pandas as pd

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchALlCandidates:
    def __init__(self):
        self.connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                         SERVER=settings.DB_SERVER,
                                         DATABASE=settings.DB_NAME,
                                         UID=settings.DB_USER,
                                         PWD=settings.DB_PASSWORD)

    def fetch_all_candidates(self):
        query = """
                SELECT TOP 25 
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
                    dcr.HTMLResumeContent,
                    jspm.JobSearchPriorityText AS JobSearchStatus,
                    cped.LinkedInProfileUrl,
                    cped.Certification,
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
                    dbo.CandidateMaster cm
                LEFT JOIN
                    dbo.CandidateContactTxn cct ON cm.CandidateID = cct.CandidateID
                LEFT JOIN 
                    dbo.AddressMaster am ON cct.AddressID = am.AddressID
                LEFT JOIN
                    dbo.ZIPCodeMaster zm ON am.ZIPCodeID = zm.ZIPCodeID
                LEFT JOIN
                    dbo.CandidatePortal cp ON cm.CandidateID = cp.CandidateID
                LEFT JOIN
                    dbo.CandidateVisa cv ON cm.CandidateID = cv.CandidateID
                LEFT JOIN
                    dbo.VisaMaster vm ON cv.VisaID = vm.VisaID
                LEFT JOIN
                    dbo.CandidateResume cr ON cm.CandidateID = cr.CandidateID
                LEFT JOIN
                    dbo.ResumeExperiences re ON cr.ResumeID = re.ResumeID
                LEFT JOIN
                    dbo.ExperienceDetail ed ON re.ExperiencesID = ed.ExperiencesID
                LEFT JOIN
                    dbo.CandidateProfessionalExperienceDetails cped ON re.ExperiencesID = cped.ExperiencesID
                LEFT JOIN
                    dbo.ExperienceJobTitle ejt ON ed.ExperienceDetailID = ejt.ExperienceDetailID 
                LEFT JOIN
                    dbo.DisplayCandidateResume dcr ON cm.CandidateID = dcr.CandidateID
                LEFT JOIN
                    dbo.CandidateJobSearchPriority cjsp ON cm.CandidateID = cjsp.CandidateID
                LEFT JOIN
                    dbo.JobSearchPriorityMaster jspm ON cjsp.JobSearchPriorityID = jspm.JobSearchPriorityID
                LEFT JOIN 
                    dbo.ResumeEducation red ON cr.ResumeID = red.ResumeID
                LEFT JOIN
                    dbo.vw_CandidateSkills vcs ON cm.CandidateID = vcs.CandidateID
                ORDER BY
                    cm.ModifiedDate DESC
        """

        df = pd.read_sql_query(query, self.connection)
        print(df, '\n\nFetched ', len(df), 'candidates from the database.')
        return
