'''
Submission grade class
'''
from .base import Base #pylint: disable=[relative-beyond-top-level]


class SubmissionGrade(Base): #pylint: disable=[too-few-public-methods]
    '''
    Submission grade class, to track all submission grade
    '''
    ATTRIBUTES = ['_id', 'assignment_id', 'cohort_member_id', 'grader_id', 'notes',
                    'total_score', 'status', 'created_by', 'updated_by', 'created_at', 'updated_at']
    REFS = ['assignment', 'grader', 'cohort_member']
    name_of_class = "submission-grades"

    def __repr__(self):
        return super().__repr__(['name','_id'])
