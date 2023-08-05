def login_template(username, password):
    template = {
        'userName': username,
        'password': password,
        'captcha': '',
        'portalType': 'CBCS'
    }
    return template


def register_course_template(student_id, subj_id, esetId, faculty_name):
    template = {
        'instId': '1',
        'stuId': student_id,
        'subjId': subj_id,
        'sxnId': '0',
        'esetId': esetId,
        'facultyName': faculty_name
    }

    return template


def drop_course_template(subj_cd,eset_id):
    template = {
        'instId': '1',
        'subjId': subj_cd,
        'sxnId': '0',
        'esetId': eset_id
    }
    return template
