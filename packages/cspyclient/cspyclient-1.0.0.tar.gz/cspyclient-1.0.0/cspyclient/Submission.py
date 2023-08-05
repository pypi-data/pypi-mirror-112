'''
Submission class
'''
from .base import Base #pylint: disable=[relative-beyond-top-level]


class Submission(Base): #pylint: disable=[too-few-public-methods]
    '''
    Submission object, to track all submissions
    '''
    ATTRIBUTES = ['_id', 'cohort_member_id', 'assignment_id',
                 'submission_url',  'email', 'name', 'answers', 'entries','created_by',
                 'updated_by', 'created_at', 'updated_at']
    REFS = ['cohort_member', 'assignment']
    name_of_class = "submissions"

    def __repr__(self):
        return super().__repr__(['name','_id'])
