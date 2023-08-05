import redis

from cumsdtu.model.lsa_model import ManageSubjectSelection
from cumsdtu.lsa_academy.logins.login import Login
from cumsdtu.templates.template import register_course_template
from cumsdtu.utils.persist_cookies import PersistCookies


class RegisterCourse(Login):
    register_course_url = "https://cumsdtu.in/LSARegistration/api/saveSchedule"

    INSIGNIFICANT_KEYS = ['electiveCoursesList', 'extraValueMap', 'helperData', 'nextStageId', 'saveDeleteRecord',
                          'sessionId','minimumRegistrationCredit', 'maximumRegistrationCredit', 'paymentDescription',
                          'creditsRegistered','showSpecializations', 'specialization1', 'specialization2', 'status', 'totalAmount',
                          'waitListed','choiceType','countVisible','credits','creditsTypeChoice','extraInfo','extraValueMap',
                          'facultyName','gradeId','headerFlag','minimumSeats','numChoice','orgStageId','prevSubjId','registrationCount','resultStatus','seats',
                          'subHeader2Flag','subHeaderFlag','substitutedCourseId','substitutedCourseLabel','totalAvailableSeats','totalSeats',
                          ]
    maps = ['courseCode', 'courseGroupLabel', 'courseId', 'courseName','registrationCount', 'totalSeats']
    heading = ['Course Code', 'Course Group Name', 'Course Id', 'Course Name', 'Seats Registered',
               'Total Seats']

    applicant_class = ManageSubjectSelection

    def __init__(self, to_verify, **kwargs):
        super().__init__(to_verify, **kwargs)
        self.to_verify = to_verify
        self.persistor = self.safe_dict(kwargs, 'persistor')
        self.student_id = self.safe_dict(kwargs, 'student_id')
        self.course_file_name = self.safe_dict(kwargs, 'course_file')

    def pre_query(self):
        result = self.find_subject_details(self.to_verify.set_code, self.to_verify.subject_id)

        if result.get('error'):
            return result

        if result.get('disabledFlag'):
            return self.custom_response(True, "Course Disabled cannot register, Course: {} set:{}".format(
                result.get('courseName'), self.to_verify.set_code), 409)

        result = self.check_registered(result)
        if result.get('status') == 1:
            return self.custom_response(True, result.get('msgLst'), 400)

        return self.query_info(result=result)

    def query_info(self, **kwargs):

        result=kwargs['result']

        payload = register_course_template(self.student_id, self.to_verify.subject_id, result.get('eset_id'),
                                           result.get('facultyName'))

        respose = self.smart_request('POST', self.register_course_url, data=payload, headers=self.headers)



        json_data = self.safe_json(respose.text)
        details = json_data.pop('data')
        self.pop_insignificant_keys(details)

        if self.course_file_name is not None:
            self.write_data(details.get('coreCoursesList'),self.course_file_name)
            return self.custom_response(False, "Course details written to {} successfully".format(self.course_file_name), 200)

        print(json_data)

        if not json_data.get('error'):
            return self.custom_response(False, json_data.get('msgLst')[-1].get('errCode'), 200, data=details)
        else:
            return self.custom_response(True, json_data.get('msgLst')[-1].get('errCode'), 400)

    @classmethod
    def extract_data(cls, db_ob, **kwargs):
        applicant = cls.applicant_class.applicant_to_object(db_ob)

        login_data = Login.do_login(applicant, **kwargs)

        if login_data.get('status') != 200:
            return login_data
        return cls(applicant, **{**login_data.pop('data'), **login_data, **kwargs}).pre_query()


def test():
    applicant = ManageSubjectSelection()
    applicant.username = '2K19/ME/051'
    applicant.password = 'April@2000'
    applicant.set_code = ''
    applicant.subject_id = 4156

    # r = redis.Redis(host='redis-13748.c14.us-east-1-2.ec2.cloud.redislabs.com',
    #                 port=13748,
    #                 password='KfhZsGRLZ0aqDzT4pl1K4BmfrFbrpaGn')

    r=redis.StrictRedis()

    persistor = PersistCookies(r, 'cumsdtu:{}'.format(applicant.username.replace('/', '_')))

    return RegisterCourse.extract_data(applicant, persistor=persistor)


if __name__ == '__main__':
    print(test())
