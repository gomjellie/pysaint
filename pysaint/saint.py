from .constants import *
from .parser import *
from . import sap_event_queue
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

import ast

class Saint:
    def __init__(self):
        self.sess = requests.Session()
        self.soup_jar = defaultdict()
        self.sess.headers = SESSION_HEADERS
        self.sess.cookies.update({'GWMESSENGER': 'stopMessenger'})

        res_init = self.sess.get(SOURCE_URL)
        self.soup_jar['init'] = BeautifulSoup(res_init.text, 'html.parser')

        form = self.soup_jar['init'].find('form', {'name': 'sap.client.SsrClient.form'})
        self.action = form.get('action')
        res_base = self.sess.post(ECC_URL + self.action)

        self.soup_jar['base'] = BeautifulSoup(res_base.text, 'lxml')

        self.sap_wd_secure_id = get_sap_wd_secure_id(self.soup_jar['base'])
        self.year_key = get_year_key(self.soup_jar['base'])
        self.semester_key = get_semester_key(self.soup_jar['base'])
        self.college_key = get_college_key(self.soup_jar['base'])
        self.faculty_key = get_faculty_key(self.soup_jar['base'])
        self.major_key = get_major_key(self.soup_jar['base'])
        self.line_key = get_line_key(self.soup_jar['base'])
        self.search_id = get_search_id(self.soup_jar['base'])

    def login(self, j_username, j_password):
        """
        log in saint.ssu.ac.kr
        :param j_username: student id
                e.g.)
                2015xxxx
        :param j_password: saint password
        :return:
        """
        self.sess.get(SAINT_URL, headers=REQUEST_HEADERS)
        res = self.sess.get(PORTAL_URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        j_salt = soup.find('input', {'name': 'j_salt'}).get('value')

        # necessary to get JSESSIONID
        self.sess.get(POPUP_URL)

        login_data = sap_event_queue.get_login_data(j_salt, j_username, j_password)

        self.sess.post(PORTAL_URL,
                       headers={'Referer': PORTAL_URL},
                       data=login_data)

        login_get = self.sess.get(
            'http://saint.ssu.ac.kr/irj/portal',
            headers={
                'Referer': PORTAL_URL,
                'Host': 'saint.ssu.ac.kr'
            })
        self.soup_jar['login_soup'] = BeautifulSoup(login_get.text, 'lxml')

        user_name = get_login_user_name(self.soup_jar['login_soup'])
        if user_name == 'fail':
            print("failed to login")
        else:
            print("log in success! user_name: {}".format(user_name))

    def get_grade(self, year=2020, semester='2 학기'):
        """
        ! login required !

        :return:
        list
        which has dictionary as it's element
        element has ['과목ID', '과목명', '이수년도', '이수학기', '학점수', '성적기호', '학술연구상태', '제외사유', '신청구분', '신청일', '승인취소일', '신청', '취소'])
        keys
        """
        self.sess.headers = SESSION_HEADERS_GRADE
        # self.sess.cookies.set_cookie(
        #     requests.cookies.create_cookie(domain='.ssu.ac.kr', name='SAPWP_active', value='1')
        # )
        sugang = self.sess.get('https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/ZCMB3W0017?sap-language=KO')
        soup = BeautifulSoup(sugang.text, 'html.parser')
        form = soup.find('form', {'name': 'sap.client.SsrClient.form'})
        action = form.get('action')
        
        dt = {
            'sap-charset': 'utf-8',
            'sap-wd-secure-id': self.sap_wd_secure_id,
            'SAPEVENTQUEUE': "ClientInspector_Notify~E002Id~E004WD01~E005Data~E004ClientWidth~003A1470px~003BClientHeight~003A946px~003BScreenWidth~003A1920px~003BScreenHeight~003A1080px~003BScreenOrientation~003Alandscape~003BThemedTableRowHeight~003A21px~003BThemedFormLayoutRowHeight~003A25px~003BDeviceType~003ADESKTOP~E003~E002ResponseData~E004delta~E005EnqueueCardinality~E004single~E003~E002~E003~E001Custom_ClientInfos~E002Id~E004WD01~E005WindowOpenerExists~E004false~E005ClientURL~E004https~003A~002F~002Fecc.ssu.ac.kr~002Fsap~002Fbc~002Fwebdynpro~002Fsap~002FZCMB3W0017~0023~E005ClientWidth~E0041470~E005ClientHeight~E004946~E005DocumentDomain~E004ssu.ac.kr~E005IsTopWindow~E004true~E005ParentAccessible~E004true~E003~E002ClientAction~E004enqueue~E005ResponseData~E004delta~E003~E002~E003~E001LoadingPlaceHolder_Load~E002Id~E004_loadingPlaceholder_~E003~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003"
        }
        grade1_1 = self.sess.post(ECC_URL + action, data=dt)
        self.soup_jar['grade1_1'] = BeautifulSoup(grade1_1.text, 'lxml')

        input_tag = soup.find('input', {'id': '_popup_url_'})
        lsdata = input_tag.get('lsdata')
        evaluated = ast.literal_eval(lsdata)[2] # ZCMB3W0017?sap-language=KO&sap-cache-buster=3B7119B0FB0A57CEFF4E4831F642E559&sap-theme=&dvc=standards&version=20151128-043535&%7eLOADING_TEMPLATE=POPUP_PAGE
        WDWL1 = self.soup_jar['grade1_1'].find_all('full-update')[1].get('windowid')
        
        update_popup = '/sap/bc/webdynpro/sap/{}&sap-wd-popupWindowID={}'.format(evaluated, WDWL1)
        grade1_2 = self.sess.get(ECC_URL + update_popup,
            headers={
                'DNT': '1',
                'Referer': 'https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/ZCMB3W0017',
                'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
                'sec-ch-ua-mobile': '?0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            }
        )
        print(ECC_URL + update_popup)
        self.soup_jar['grade1_2'] = BeautifulSoup(grade1_2.text, 'html.parser')
        
        close_key = get_close_key(self.soup_jar['grade1_1'])
        print(close_key)
        close_event = sap_event_queue.button_press(close_key, self.sap_wd_secure_id)
        print(ECC_URL + action)
        print(close_event)

        # print(self.sess.cookies)
        grade2 = self.sess.post(ECC_URL + action, data=close_event)
        print(grade2.status_code, grade2._content)
        # print(self.sess.headers)
        print(grade2, grade2.text) # 여기서 출력값이 이상함
        self.soup_jar['grade2'] = BeautifulSoup(grade2.text, 'lxml')

        year_key = get_year_key_from_grade(self.soup_jar['grade2'])
        year_skey = get_year_skey_from_grade(self.soup_jar['grade2'], year)
        semester_key = get_semester_key_from_grade(self.soup_jar['grade2'])
        semester_skey = get_semester_skey_from_grade(self.soup_jar['grade2'], semester)
        
        year_select_event = sap_event_queue.combo_select(year_key, year_skey, self.sap_wd_secure_id)
        self.sess.post(ECC_URL + action, data=year_select_event)
        semester_select_event = sap_event_queue.combo_select(semester_key, semester_skey, self.sap_wd_secure_id)
        table = self.sess.post(ECC_URL + action, data=semester_select_event)
        print(table.text)

        # grade_card = parse_grade_card(self.soup_jar['grade_table'])
        return

    def select_year(self, year):
        """
        :param year:
        :type year: String
        """

        dt_year = sap_event_queue.combo_select(self.year_key, year, self.sap_wd_secure_id)
        pg_year = self.sess.post(ECC_URL + self.action, data=dt_year)

    def select_semester(self, semester):
        """
        학기를 선택한다.
        :param semester:
        :type semester: str
                example) '1 학기', '여름학기', '2 학기', '겨울학기'
        """

        semester_skey = get_semester_skey(self.soup_jar['base'], semester)
        dt_semester = sap_event_queue.combo_select(self.semester_key, semester_skey, self.sap_wd_secure_id)

        after_semester_click = self.sess.post(ECC_URL + self.action, data=dt_semester)
        self.soup_jar['semester'] = BeautifulSoup(after_semester_click.text, 'lxml')

    def select_course_section(self, section):
        """
        학부전공별, 교양필수, 교양선택등 이 있는 탭을 선택한다
        :param section:
        :type section: str
                example) '교양필수', '교양선택',
        """

        section_id = get_section_id(self.soup_jar['base'])
        tab_id = get_tab_id(self.soup_jar['base'], section)
        item_index = get_tab_item_index(self.soup_jar['base'], section)
        dt_tab = sap_event_queue.tab_select(section_id, tab_id, item_index, self.sap_wd_secure_id)

        after_course_section_click = self.sess.post(
            ECC_URL + self.action, data=dt_tab)
        self.soup_jar['{}'.format(section)] = BeautifulSoup(after_course_section_click.text, 'lxml')

    def _select_college(self, college):
        """
        단과대학을 선택한다.
        :param college:
        :type college: str
                example) 인문대학, IT대학, ..
        """

        college_skey = get_college_skey(self.soup_jar['semester'], college)
        dt_college = sap_event_queue.combo_select(self.college_key, college_skey, self.sap_wd_secure_id)

        after_college_click = self.sess.post(ECC_URL + self.action, data=dt_college)

        self.soup_jar['college'] = BeautifulSoup(after_college_click.text, 'lxml')

    def _select_faculty(self, faculty):
        """
        학부를 선택한다.
        :param faculty:
        String
        철학과, 정보통신전자공학부, ...
        :return:
        """

        faculty_skey = get_faculty_skey(self.soup_jar['college'], faculty)
        dt_faculty = sap_event_queue.combo_select(self.faculty_key, faculty_skey, self.sap_wd_secure_id)

        after_faculty_click = self.sess.post(ECC_URL + self.action, data=dt_faculty)
        self.soup_jar['faculty'] = BeautifulSoup(after_faculty_click.text, 'lxml')

    def _select_major(self, major):
        """
        학과 선택과 동시에 search_button을 눌러서 subjects 정보를 받아온다
        :param major:
        :type major: str
        '정보통신전자공학부'
        :return type: list
        """

        major_skey = get_major_skey(self.soup_jar['faculty'], major)
        dt_major = sap_event_queue.combo_select_with_button_press(self.major_key, major_skey, self.search_id, self.sap_wd_secure_id)
        after_search_click = self.sess.post(ECC_URL + self.action, data=dt_major)

        self.soup_jar['search'] = BeautifulSoup(after_search_click.text, 'lxml')
        subjects = parse_subjects(self.soup_jar['search'])

        return subjects

    def _select_uni_faculty_major(self, major):
        """
        학부가 1개밖에 없는 학과를 선택함
        soup_jar['faculty']가 없어서 따로 처리해줌

        :param major:
        스포츠학부

        :return type: list
        """

        major_skey = get_major_skey(self.soup_jar['college'], major)
        dt_major = sap_event_queue.combo_select_with_button_press(self.major_key, major_skey, self.search_id,
                                                                  self.sap_wd_secure_id)
        after_search_click = self.sess.post(ECC_URL + self.action, data=dt_major)

        self.soup_jar['search'] = BeautifulSoup(after_search_click.text, 'lxml')
        subjects = parse_subjects(self.soup_jar['search'])

        return subjects

    def _select_search_button(self):
        """
        학부에 학과가 1개일 경우 학과를 선택하지 않고 이 메소드를 호출한다.
        바로 search press event 를 전송해서 정보를 받아 올 수 있다.

        :return type: list
        """

        dt_click_search = sap_event_queue.button_press(self.search_id, self.sap_wd_secure_id)
        after_search_click = self.sess.post(ECC_URL + self.action, data=dt_click_search)

        self.soup_jar['search'] = BeautifulSoup(after_search_click.text, 'lxml')
        subjects = parse_subjects(self.soup_jar['search'])

        return subjects

    def select_on_major(self, college, faculty, major):
        """
        :param college: 단과대학
        :param faculty: 학부
        :param major: 학과
        :return type: list
        """

        if major == '':
            return None

        self._select_college(college)
        faculties = get_faculties(self.soup_jar['college'])

        if len(faculties) == 1:
            # 스포츠학부 같은 경우 단과대학 선택후 학부가 1개라서 바로 학부가 선택됨
            majors = get_majors(self.soup_jar['college'])
            if major in majors:
                return self._select_uni_faculty_major(major)
            else:
                print("major: {} is not in majors: {}".format(major, majors))
                return None
        else:
            self._select_faculty(faculty)
            majors = get_majors(self.soup_jar['faculty'])
        if len(majors) == 1:
            return self._select_search_button()

        return self._select_major(major)

    def _select_grade(self, grade):
        """
        교양필수 탭에서 학년을 선택한다.
        선행작업:
        CourseParser.select_year()
        CourseParser.select_semester()
        CourseParser.select_course_section()

        :param grade:
        '전체학년', '1학년', '2학년', '3학년', '4학년', '5학년'

        :return: soup
        """

        grade_id = get_grade_id_from_liberal_arts_tab(self.soup_jar['교양필수'])
        grade_skey = get_grade_skey_from_liberal_arts_tab(self.soup_jar['교양필수'], grade)
        dt_grade = sap_event_queue.combo_select(grade_id, grade_skey, self.sap_wd_secure_id)

        after_select_grade = self.sess.post(
            ECC_URL + self.action, data=dt_grade
        )
        grade_soup = BeautifulSoup(after_select_grade.text, 'lxml')
        self.soup_jar['grade'] = grade_soup

        return grade_soup

    def _select_selective_liberal_course(self, course_name):
        """
        교양선택에서 과목을 선택하고 검색 버튼을 누른다.
        선행작업:
        CourseParser.select_course_section('교양선택')
        :param course_name:
        '전체', '*문학과 예술',
        :return:
        """

        course_id = get_selective_id(self.soup_jar['교양선택'])
        course_skey = get_selective_course_skey(self.soup_jar['교양선택'], course_name)
        search_id = get_search_id(self.soup_jar['교양선택'])
        dt_combo_with_search_button_press \
            = sap_event_queue.combo_select_with_button_press(course_id, course_skey, search_id, self.sap_wd_secure_id)
        on_selective_liberal_course = self.sess.post(ECC_URL + self.action, data=dt_combo_with_search_button_press)
        self.soup_jar['selective_search'] = BeautifulSoup(on_selective_liberal_course.text, 'lxml')

        return parse_subjects(self.soup_jar['selective_search'])

    def _select_liberal_arts(self, course_name):
        """
        선행작업:
        CoursePraser._select_grade()
        교양필수 과목명을 선택하고 검색버튼을 누른다.
        :param course_name:
        '컴퓨팅적사고'
        :return:
        """

        search_id = get_search_id(self.soup_jar['교양필수'])
        course_key = get_liberal_arts_key(self.soup_jar['교양필수'])
        course_skey = get_liberal_arts_skey(self.soup_jar['교양필수'], course_name)
        dt_combo_with_search_button_press \
            = sap_event_queue.combo_select_with_button_press(course_key, course_skey, search_id, self.sap_wd_secure_id)
        on_liberal_arts_search_click = self.sess.post(ECC_URL + self.action, data=dt_combo_with_search_button_press)
        self.soup_jar['liberal_search'] = BeautifulSoup(on_liberal_arts_search_click.text, 'lxml')

        return parse_subjects(self.soup_jar['liberal_search'])

    def select_on_liberal_arts(self, course_name):
        """
        :param course_name:
        :return:
        subject lists
        """

        # self._select_grade(grade)
        courses = get_liberal_arts_courses(self.soup_jar['교양필수'])
        if course_name not in courses:
            raise Exception()

        return self._select_liberal_arts(course_name)

    def select_on_selective_liberal(self, course_name):
        """
        교양선택에서 과목을 선택해서 검색 정보를 얻는다
        선행작업:
        CourseParser.select_course_section('교양선택')
        :param course_name:
        '전체', '*문학과 예술(융합-인문)', ...
        :return:
        """
        return self._select_selective_liberal_course(course_name)

    def select_line(self, line):
        """
        줄수/페이지 수를 바꾼다
        :param line:
        Line.TEN, Line.TWENTY, Line.FIFTY, ...
        :return:
        """
        if not Line.has_value(line):
            raise ValueError("select_line() got wrong arguments line: {}\n"
                             "line should be one of {}".format(line, Line.list()))

        dt_combo_select = sap_event_queue.combo_select(self.line_key, line, self.sap_wd_secure_id)
        after_line_click = self.sess.post(ECC_URL + self.action, data=dt_combo_select)

    def get_liberal_arts_map(self):
        """
        학년, 교양필수_과목 맵을 얻는다.
        선행되야하는 작업:
        CourseParser.select_course_section('교양필수')
        CourseParser.select_year()
        CourseParser.select_semester()
        :return:
        [

        ]
        """

        self.select_course_section('교양필수')
        liberals = get_liberal_arts_courses(self.soup_jar['교양필수'])

        return liberals

    def get_major_map(self):
        """
        단과대 학부 전공 맵을 얻는다.
        선행되야하는 작업:
        CourseParser.select_year()
        CourseParser.select_semester()
        :return:
        {
            '인문대학': {
                '철학과': ['철학과'],
                ...
            },
            'IT대학': {
                '정보통신전자공학부': ['정보통신전자공학부', '전자공학과'],
                ...
            },
            ...
        }
        """

        self._select_college('인문대학')
        colleges = get_colleges(self.soup_jar['college'])
        selection_map = {key: {} for key in colleges}
        for college in colleges:
            self._select_college(college)
            faculties = get_faculties(self.soup_jar['college'])
            faculties_map = {key: {} for key in faculties}
            selection_map[college] = faculties_map
            for faculty in faculties:
                if len(faculties) == 1:
                    majors = get_majors(self.soup_jar['college'])
                else:
                    self._select_faculty(faculty)
                    majors = get_majors(self.soup_jar['faculty'])
                selection_map[college][faculty] = majors

        return selection_map

    def get_selective_liberal_map(self):
        """
        :TODO :
        CourseParser.select_course_section('교양선택') 을 처음 실행해서 얻게된
        self.soup_jar['교양선택'] 에 과목정보가 있는경우가 있고 없는경우가 있다.
        과목정보가 변경되면 과목정보가 생기고 그대로면 안생기는듯
        교양선택 맵을 얻는다.
        선행되야하는 작업:
        :return:
        """

        self.select_course_section('교양선택')
        courses = get_selective_courses(self.soup_jar['교양선택'])

        return courses


if __name__ == '__main__':
    course_parser = Saint()
    course_parser.select_year('2017')
    course_parser.select_semester('1 학기')
    results = course_parser.select_on_major('인문대학', '철학과', '철학과')

    print(results)

