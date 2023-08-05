'''Cohort class'''
from .base import Base #pylint: disable=[relative-beyond-top-level]
from .student import Student #pylint: disable=[relative-beyond-top-level]
from .utils import Utils #pylint: disable=[relative-beyond-top-level]


class Cohort(Base):
    '''
    Cohort object to manage all cohorts
    '''
    ATTRIBUTES = ['_id', 'course', 'course_id', 'name', 'slug', 'contact_list_sheet_url',
                 'support_email', 'prework_url', 'start_date', 'demo_day_date',
                  'created_by', 'updated_by', 'created_at', 'updated_at']
    REFS = ['course']
    name_of_class = 'cohorts'

    def __repr__(self):
        return super().__repr__(['name','_id'])

    def enroll_single_student(self, student, status='PARTICIPANT'):
        '''
        Add a new student information to database
        Parameter:
            student: Student object include data of students to be added
            status: status of the current student in cohort (default 'PARTICIPANT')
        '''
        if type(student) is not Student:
            print('ERROR: Data must be instance of Student')
            return
        if not getattr(self, '_id', ''):
            print('ERROR: Cohort undefined')
            return
        if not getattr(student, '_id', ''):
            print('ERROR: Student undefined')
            return
        data = {'cohortId': self._id, 'memberType':'Student', 'memberId':student._id,
                'status': status}
        self.db_service.post('/cohort-members', data)

    def enroll_students(self, students, status='PARTICIPANT'):
        '''
        Add multiple students information to database
        Parameter:
            students: Multiple student object in a iterable type, include data of students to
            be added
            status: status of the current students in cohort (default 'PARTICIPANT')
        '''
        for student in students:
            self.enroll_single_student(student, status)

    def get_student_list(self, output='DataFrame'):
        '''
        Get student information in the current cohort from database
        Parameter:
            output: kind of multi-value class to holder the result. the default is 'DataFrame'
        Return: result in corresponding output type, each single item is in Student object type
        '''
        if not getattr(self, '_id', ''):
            print('ERROR: Cohort undefined')
            return
        students = self.db_service.get(f'/cohorts/{self._id}/students?page=1&limit=1000')['students']
        return Utils.output_form(Student, students, output)

    @classmethod
    def find_one_by_name(cls, the_name):
        '''
        Get the first value of the class that match a key, with default key is its 'name'
        Parameter:
            the_name: the current key in query
        Return: result in current object type
        '''
        return cls.find_one(filter_={'name': the_name})
