'''
Class Assignment
'''
from .base import Base #pylint: disable=[relative-beyond-top-level]


class Assignment(Base): #pylint: disable=[too-few-public-methods]
    '''
    Assignment object, to manage all test assginments
    '''
    ATTRIBUTES = ['_id', 'name', 'slug', 'cohort_id', 'assignment_type',
                  'questions', 'assignment_url', 'max_progress_score', 'member_only',
                  'created_by', 'updated_by', 'created_at', 'updated_at']
    REFS = ['cohort']
    name_of_class = "assignments"

    def __repr__(self):
        return super().__repr__(['name','_id'])

    @classmethod
    def find_one_by_name(cls, the_name):
        '''
        Get the first value of the class that match a key, with default key is its 'name'
        Parameter:
            the_name: the current key in query
        Return: result in current object type
        '''
        return cls.find_one(filter_={'name':the_name})
