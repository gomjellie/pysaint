"""
    parser for saint

    __        __               _               _   _
    \ \      / /_ _ _ __ _ __ (_)_ __   __ _  | | | |
     \ \ /\ / / _` | '__| '_ \| | '_ \ / _` | | | | |
      \ V  V / (_| | |  | | | | | | | | (_| | |_| |_|
       \_/\_/ \__,_|_|  |_| |_|_|_| |_|\__, | (_) (_)
                                       |___/


     _   _                      ____
    | \ | | ___   ___  _ __    / ___| __ _ _ __   __ _
    |  \| |/ _ \ / _ \| '_ \  | |  _ / _` | '_ \ / _` |
    | |\  | (_) | (_) | | | | | |_| | (_| | | | | (_| |
    |_| \_|\___/ \___/|_| |_|  \____|\__,_|_| |_|\__, |
                                                 |___/

    눈갱 주의
"""

from bs4 import element
import re
import ast


def get_login_user_name(login_soup):
    """
    return user's korean name
    :param login_soup:
    self.soup_jar['login_soup']
    :return:
    """
    name_span = login_soup.find('span', {'class': 'fontS01'})
    if name_span is None:
        return 'fail'

    return name_span.text


def parse_grade_card(grade_table_soup):
    """
    get user's grade card
    :param grade_table_soup:
    soup_jar['grade_table']
    :return:
    list
    which has dictionary as it's element
    element has ['과목ID', '과목명', '이수년도', '이수학기', '학점수', '성적기호', '학술연구상태', '제외사유', '신청구분', '신청일', '승인취소일', '신청', '취소'])
    keys

    """
    tbody = grade_table_soup.find('tbody', {'id': 'WD15-contentTBody'})
    th = tbody.find_all('th')
    tr = tbody.find_all('tr')

    headers = [each.text for each in th]
    # ['과목ID', '과목명', '이수년도', '이수학기', '학점수', '성적기호', '학술연구상태', '제외사유', '신청구분', '신청일', '승인취소일', '신청', '취소']

    tds = [each for each in tr]
    subjects = []
    for td in tds[1:]:
        cell = [cell.text for cell in td]
        subjects.append(cell)

    ret = []
    for subject in subjects:
        single = dict((headers[i], subject[i]) for i in range(len(subject)))
        ret.append(single)

    return ret


def get_tab_item_index(base_soup, section):
    """
    ItemIndex 를 얻는다.
    :param elem:
    Saint.soup_jar['base']
    :param section:
    '학부전공별', '교양필수', '교양선택', ...
    :return:
    """
    elem = base_soup.find('span', text=section).parent.parent
    lsdata = elem.get('lsdata')
    lsdata = lsdata.replace('true', 'True')
    lsdata_dict = ast.literal_eval(lsdata)
    return lsdata_dict[1]


def get_skey(elem):
    if type(elem) == element.Tag:
        skey_yaml = elem.get('lsdata')
        return ast.literal_eval(skey_yaml)[0]
    else:
        raise Exception("Unexpected elem type {}".format(type(elem)))


def get_liberal_arts_key(soup_grade):
    """
    :param soup_grade:
    Saint.soup_jar['grade']
    :return:
    'WD01C2'
    """
    label = soup_grade.find('label', text='과목명')
    return label.get('f')


def get_selective_id(soup_selective):
    """
    교양선택 탭에서 분야의 Id를 얻는다
    :param soup_selective:
    Saint.soup_jar['교양선택']
    :return:
    """
    label = soup_selective.find('label', text='분야')
    return label.get('f')


def get_year_key(soup_base):
    label = soup_base.find('label', text='학년도')
    year_key = label.get('f')
    return year_key


def get_semester_key(soup_base):
    label = soup_base.find('label', text='학기')
    semester_key = label.get('f')
    return semester_key


def get_sap_wd_secure_id(soup_base):
    form = soup_base.find('form', {'id': 'sap.client.SsrClient.form'})
    secure_id = form.find('input', {'id': 'sap-wd-secure-id'})
    sap_wd_secure_id = secure_id.get('value')
    return sap_wd_secure_id


def get_selective_course_skey(selective_soup, course_name):
    course_td = selective_soup.find('td', text=course_name)
    course_tr = course_td.parent
    course_yaml = course_tr.get('lsdata')
    course_skey = ast.literal_eval(course_yaml)[0]
    return course_skey


def get_semester_skey(soup_base, semester):
    if semester in ['1 학기', '여름학기', '2 학기', '겨울학기']:
        semester = soup_base.find('tr', text=semester)
        skey_yaml = semester.get('lsdata')
        semester_skey = ast.literal_eval(skey_yaml)[0]
        return semester_skey
    else:
        raise Exception(
            "parameter semester is expected in ['1 학기', '여름학기', '2 학기', '겨울학기'] but {} token".format(semester))


def get_faculty_key(soup_base):
    faculty = soup_base.find('input', {"lsdata": re.compile(r"{1:'2.2em',8:"),
                                     "lsevents": "{Select:[{ResponseData:'delta',ClientAction:'submit'},{}]}"})
    faculty_key = faculty.get('id')
    return faculty_key


def get_college_key(soup_base):
    col_input = soup_base.find('input', {"lsdata": re.compile(r"{1:'14.3em',")})  # 단과대학
    college_key = col_input.get('id')
    return college_key


def get_major_key(soup_base):
    major = soup_base.find('input', {"lsdata": re.compile(r"{1:'2.2em',8:"),
                                      "lsevents": "{Select:[{ResponseData:'delta',EnqueueCardinality:'single'},{}]}"})
    major_key = major.get('id')
    return major_key


def get_liberal_arts_skey(soup_grade, course_name):
    """
    :param soup_grade:
    Saint.soup_jar['grade']
    :param course_name:
    '컴퓨팅적사고'
    :return:
    """
    course_elem = soup_grade.find('td', text=course_name).parent
    course_skey = get_skey(course_elem)
    return course_skey


def get_major_skey(soup_major, major):
    major_skey_elem = soup_major.find_all('tr', text=major)
    major_skey_elem = major_skey_elem[len(major_skey_elem) - 1]
    major_skey = get_skey(major_skey_elem)
    return major_skey


def get_search_id(soup_base):
    search_elem = soup_base.find("div", {"lsdata": re.compile(r"{0:'검색',4:'찾기',10:")})
    search_id = search_elem.get('id')
    return search_id


def get_college_skey(soup_base, college):
    """
    :param soup_base:
    Saint.soup_jar['semester']
    :param college:
    :return:
    """
    col_elem = soup_base.find('tr', text=college)  # 인문대학 법과대학 등등....
    col_skey = get_skey(col_elem)
    return col_skey


def get_faculty_skey(soup_faculty, faculty):
    faculty_skey_elem = soup_faculty.find('tr', text=faculty)
    faculty_skey = get_skey(faculty_skey_elem)
    return faculty_skey


def parse_subjects(search_soup):
    """
    :param search_soup:
    SoupParser.soup_jar['search']
    :return:
    list
    subjects
    """
    subjects = []
    th = search_soup.select('th')
    tr = search_soup.find_all('tr', {'role': 'row'})

    keys = [key.text for key in th]
    for row in tr:
        cells = row.find_all('td')
        if len(cells) == 1:
            return subjects
        subject = dict((keys[i], cells[i].get_text("\n")) for i in range(15))
        subjects.append(subject)
    return subjects


def get_liberal_arts_courses(grade_soup):
    """
    :param grade_soup:
    SoupParser.soup_jar['grade']
    :return:
    """
    content = grade_soup.find('content')
    divs = content.find_all('div', {'class': 'lsItemlistbox__root'})
    if len(divs) != 2:
        raise Exception()

    course_divs = divs[1]
    tds = course_divs.find_all('td')
    liberal_arts_courses = []
    for td in tds:
        liberal_arts_courses.append(td.text)
    return liberal_arts_courses


def get_colleges(semester_soup):
    """
    college를 아무거나 선택해서 soup_jar['college']를 확보한후 실행한다.
    :param semester_soup:
    SoupParser.soup_jar['college']
    :return:
    [
    '인문대학',
    '자연과학대학',
    '법과대학',
    '사회과학대학',
    '경제통상대학',
    '경영대학',
    '공과대학',
    'IT대학',
    '베어드학부대학',
    '예술창작학부',
    '스포츠학부',
    '융합특성화자유전공학부']
    """
    content = semester_soup.find('content')
    college_div = content.find('div')
    tds = college_div.tbody.find_all('td')
    colleges = []
    for td in tds:
        colleges.append(td.text)
    return colleges


def get_faculties(college_soup):
    """
    :param college_soup:
     SoupParser.soup_jar['college']
    :return:
    ['전자정보공학부 전자공학전공',
    '전자정보공학부 IT융합전공',
    '컴퓨터학부',
    '소프트웨어학부',
    '정보통신전자공학부',
    '스마트시스템소프트웨어학과',
    '글로벌미디어학부',
    '미디어경영학과']
    """
    content = college_soup.find('content')
    first_div = content.find('div')
    siblings = first_div.find_next_siblings()
    if len(siblings) == 2:
        major_div = first_div.find_next_siblings()[0]
        tds = major_div.tbody.find_all('td')
        faculties = []
        for td in tds:
            faculties.append(td.text)
        return faculties
    else:
        raise Exception()


def get_majors(faculty_soup):
    """
    :param faculty_soup:
    SoupParser.soup_jar['faculty']
    :return:
    """
    content = faculty_soup.find('content')
    first_div = content.find('div')
    siblings = first_div.find_next_siblings()
    if len(siblings) == 2:
        major_div = first_div.find_next_siblings()[1]
        tds = major_div.tbody.find_all('td')
        majors = []
        for td in tds:
            majors.append(td.text)
            if '' in majors:
                majors.remove('')
        return majors
    else:
        raise Exception()


def get_selective_courses(selective_soup):
    """
    :param selective_soup:
    self.soup_jar['교양선택']
    :return:
    """
    course_td = selective_soup.find('td', text='전체')
    course_tr = course_td.parent
    nexts = course_tr.find_next_siblings()
    prevs = course_tr.find_previous_siblings()
    courses = ['전체']
    for n in nexts:
        courses.append(n.text.strip())
    for p in prevs:
        courses.append(p.text.strip())

    return courses


def get_section_id(base_soup):
    """
    학부전공별, 교양필수, 교양선택 등 항목을 선택하는데 필요한 id를 얻는다
    :param base_soup:
    SoupParser.soup_jar['base']
    :return:
    """
    table = base_soup.find('table', {
        'lsevents': "{TabSelect:[{ResponseData:'delta',ClientAction:'submit'},{}]," +
                    "Scroll:[{ResponseData:'delta',EnqueueCardinality:'single'},{}]," +
                    "Hotkey:[{ResponseData:'delta',ClientAction:'submit'},{}]}"
    })
    return table.get('id')


def get_tab_id(base_soup, tab_name):
    """
    학부전공별, 교양필수, 교양선택등 이 있는 탭의 id를 얻는다
    :param base_soup:
    SoupParser.soup_jar['base']
    :param tab_name:
    '학부전공별', '교양필수', '교양선택', ...
    :return:
    """
    tab_span = base_soup.find('span', text=tab_name)
    return tab_span.parent.parent.get('id')


def get_grade_id_from_liberal_arts_tab(liberal_arts_soup):
    """
    :param liberal_arts_soup:
    SoupParser.soup_jar['교양선택']
    :param grade:
    '전체학년', '1학년', '2학년', '3학년', '4학년', '5학년'
    :return:
    """
    # tr = liberal_arts_soup.find('tr', text=grade)
    # return tr.get('id')
    return liberal_arts_soup.find('span', text='과목 수준').label.get('f')


def get_grade_skey_from_liberal_arts_tab(liberal_arts_soup, grade):
    """
    :param liberal_arts_soup:
    SoupParser.soup_jar['교양선택']
    :param grade:
    '전체학년', '1학년', '2학년', '3학년', '4학년', '5학년'
    :return:
    """
    tr = liberal_arts_soup.find('tr', text=grade)
    lsdata = tr.get('lsdata')
    lsdata_dict = ast.literal_eval(lsdata)
    return lsdata_dict[0]

