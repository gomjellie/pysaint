"""
    End User를 위한 간단한 api


"""

from .saint import Saint
import copy
from tqdm import tqdm


def get(course_type, year_range, semesters, **kwargs):
    """
    THIS IS THE END POINT OF pysaint API
    USAGE::

        >>> import pysaint
        >>> res = pysaint.get('전공', ['2018'], ['2 학기'])
        >>> print(res)


        >>> res = pysaint.get('교양필수', range(2015, 2017), ['1 학기', '여름학기', '2 학기', '겨울학기'])
        >>> print(res)


        >>> res = pysaint.get('교양선택', (2016, 2017, 2018), ('1 학기', ))
        >>> print(res)

    :param course_type:
    :type course_type: str
    example )
            '교양필수'
            '전공'
            '교양선택'
    :param year_range:
    :type year_range: list or tuple or range or str or int
    example )
            '2018'
            ['2018']
            [2018]
            ['2017', '2018']
            [2017, 2018]
            (2015, 2016, 2017)
            ('2016', '2017', '2018')
            range(2015, 2019)
    :param semesters:
    :type semesters: list or tuple or str
    example )
            '1 학기'
            ['1 학기', '여름학기', '2 학기', '겨울학기']
            ('1 학기', '2 학기', )

    :param silent: decide progress bar silent or not
    :return: dict
    """

    if type(year_range) not in (tuple, list, range, str, int):
        raise ValueError("get() got wrong arguments year_range: {}\n"
                         "expected tuple type or list, or range type but got {} type".format(year_range, type(year_range)))

    if type(semesters) not in (tuple, list, str):
        raise ValueError("get() got wrong arguments semesters: {}\n"
                         "expected tuple type or list type but got {} type".format(semesters, type(semesters)))

    if type(year_range) in (str, int):
        year_range = [year_range]

    if type(semesters) is str:
        semesters = [semesters]

    reformed_year_range = []
    for year in year_range:
        if 2000 < int(year) < 2020:
            pass
        else:
            raise ValueError("get() got wrong arguments year_range: {}\n"
                             "expected to be in year range(2000, 2020) but got {}".format(year_range, int(year)))
        reformed_year_range.append("{}".format(year))

    if course_type == '교양필수':
        return _liberal_arts(year_range=reformed_year_range, semesters=semesters, **kwargs)
    elif course_type == '전공':
        return _major(year_range=reformed_year_range, semesters=semesters, **kwargs)
    elif course_type == '교양선택':
        return _selective_liberal(year_range=reformed_year_range, semesters=semesters, **kwargs)
    else:
        raise ValueError("get() got wrong arguments course_type: {} \n"
                         "expected to get '교양필수', '전공', '교양선택'".format(course_type))


def grade(id, password=None):
    """
    get grade card from saint.ssu.ac.kr
    :param id: student id
            e.g.) 2015xxxx
    :param password: saint password
    :return:
    list
    """
    saint = login(id, password)
    grade_card = saint.get_grade()
    return grade_card


def _liberal_arts(year_range=[], semesters=[], silent=False):
    """
    교양필수 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :type year_range: list or tuple
    example input )
            [2013, 2014, 2015, 2016, 2017, 2018]
            or
            (2017, 2018)
    :param semesters:
    :type semesters: list or tuple
    example input )
            ['1 학기', '여름학기', '2 학기', '겨울학기']
            or
            ('1 학기')
    :return:
    {
        2013: {
            '전체학년': {
                'CHAPEL': [
                    {
                        dictionary which has
                        dict_keys(['계획', '이수구분(주전공)',
                        '이수구분(다전공)', '공학인증', '교과영역',
                        '과목번호', '과목명', '분반', '교수명',
                        '개설학과', '시간/학점(설계)', '수강인원',
                        '여석', '강의시간(강의실)', '수강대상'])
                    }
                ],
                '컴퓨터활용1(Excel)': [],
                '컴퓨터활용2(PPT)': [],
                'Practical Reading ＆ Writing': [],
                '현대인과성서2': []
                }
            }
            '1학년': {...},
            '2학년': {...},
            '3학년': {...},
            '4학년': {...},
            '5학년': {...}
        },
        year: {
            grade: {
                course_name: [] <- list which has dictionaries as it's elements
            }
        }
    }
    """
    ret = {year: {} for year in year_range}
    saint = Saint()
    saint.select_course_section('교양필수')

    def __get_whole_course(year, semester):
        saint.select_year(year)
        saint.select_semester(semester)
        liberal_map = saint.get_liberal_arts_map()
        course_map = copy.deepcopy(liberal_map)

        for grade in liberal_map:
            course_map[grade] = {course_name: {} for course_name in liberal_map[grade]}

        pbar = tqdm(liberal_map, disable=silent)
        for grade in pbar:
            pbar.set_description("Processing {:8s}".format(grade))
            for course_name in liberal_map[grade]:
                if course_name != '':
                    course_map[grade][course_name] = saint.select_on_liberal_arts(grade, course_name)

        return course_map

    year_bar = tqdm(year_range, disable=silent)
    for year in year_bar:
        year_bar.set_description("Year: {:4s}".format(year))
        semester_bar = tqdm(semesters, disable=silent)
        for semester in semester_bar:
            semester_bar.set_description("Semester: {:6s}".format(semester))
            course_bunch = __get_whole_course(year, semester)
            ret[year][semester] = course_bunch

    return ret


def _major(year_range=[], semesters=[], silent=False):
    """
    전공 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :type year_range: list or tuple
    :param semesters:
    :type semesters: list or tuple
    :return:
    {
        '2017': {
            '1 학기': {
                '인문대학': {
                    '중어중문학과': {
                        '중어중문학과': [
                            {
                                '계획': '\xa0',
                                '이수구분(주전공)': '전선-중문',
                                '이수구분(다전공)': '복선-중문/부선-중문',
                                '공학인증': '\xa0',
                                '교과영역': '7+1교과목\n인턴쉽(장기과정)\n인턴쉽',
                                '과목번호': '5010611601',
                                '과목명': '국내장기현장실습(3)',
                                '분반': '\xa0',
                                '교수명': '\xa0',
                                '개설학과': '경력개발팀',
                                '시간/학점(설계)': '3.00 /3',
                                '수강인원': '1',
                                '여석': '199',
                                '강의시간(강의실)': '\xa0',
                                '수강대상': '전체'
                            },
                            {
                                ...
                                dict_keys(['계획', '이수구분(주전공)', '이수구분(다전공)', '공학인증', '교과영역',
                                '과목번호', '과목명', '분반', '교수명', '개설학과', '시간/학점(설계)', '수강인원',
                                '여석', '강의시간(강의실)', '수강대상'])
                            }
                        ]
                    },
                    '국어국문학과': {},
                    '일어일문학과': {},
                    '영어영문학과': {},
                    '불어불문학과': {},
                    '철학과': {},
                    '사학과': {},
                    '기독교학과': {},
                },
                '자연과학대학': {},
                '법과대학': {},
                '사회과학대학': {},
                '경제통상대학': {},
                '경영대학': {},
                '공과대학': {},
                'IT대학': {},
                '베어드학부대학': {},
                '예술창작학부': {},
                '스포츠학부': {},
                '융합특성화자유전공학부': {}
            }
        },
        'year': {
            'semester': {
                'college': {
                    'faculty': {
                        'major': [
                            {
                                dict_keys(['계획', '이수구분(주전공)', '이수구분(다전공)', '공학인증', '교과영역',
                                '과목번호', '과목명', '분반', '교수명', '개설학과', '시간/학점(설계)', '수강인원',
                                '여석', '강의시간(강의실)', '수강대상'])
                            }
                        ]
                    }
                }
            }
        }
    }
    """

    ret = {year: {} for year in year_range}
    saint = Saint()

    def __get_whole_course(year, semester):
        saint.select_year(year)
        saint.select_semester(semester)
        major_map = saint.get_major_map()
        course_map = copy.deepcopy(major_map)

        for college in major_map:
            for faculty in major_map[college]:
                course_map[college][faculty] = {key: [] for key in major_map[college][faculty]}

        college_bar = tqdm(major_map, disable=silent)
        for college in college_bar:
            college_bar.set_description("Processing {:8s}".format(college))
            faculty_bar = tqdm(major_map[college], disable=silent)
            for faculty in faculty_bar:
                faculty_bar.set_description_str("Processing {:8s}".format(faculty))
                for major in major_map[college][faculty]:
                    course_map[college][faculty][major] = saint.select_on_major(college, faculty, major)

        return course_map

    year_bar = tqdm(year_range, disable=silent)
    for year in year_bar:
        year_bar.set_description("Year: {:4}".format(year))
        semester_bar = tqdm(semesters, disable=silent)
        for semester in semester_bar:
            semester_bar.set_description_str("Semester: {:6}".format(semester))
            course_bunch = __get_whole_course(year, semester)
            ret[year][semester] = course_bunch

    return ret


def _selective_liberal(year_range=[], semesters=[], silent=False):
    """
    교양선택 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :return: dict
    {
        2017: {
            '1 학기': {
                전체: [
                    {
                        '계획': '\xa0',
                        '이수구분(주전공)': '교선',
                        '이수구분(다전공)': '\xa0',
                        '공학인증': '\xa0',
                        '교과영역': '*세계의언어(핵심-창의)\n(기초역량-국제어문)영어',
                        '과목번호': '2150017601',
                        '과목명': 'Advanced Writing and speaking English I',
                        '분반': '\xa0',
                        '교수명': '이종일\n이종일\n이종일',
                        '개설학과': '벤처경영학과(계약학과)',
                        '시간/학점(설계)': '3.00 /3',
                        '수강인원': '11',
                        '여석': '39',
                        '강의시간(강의실)': '월 19:00-19:50 (조만식기념관 12530-이종일)\n월 20:00-20:50 (조만식기념관 12530-이종일)\n월 21:00-21:50 (조만식기념관 12530-이종일)',
                        '수강대상': '전체학년 벤처경영학과(계약학과) (대상외수강제한)(대상외수강제한)'
                    },
                    {
                        dict_keys(['계획', '이수구분(주전공)', '이수구분(다전공)',
                        '공학인증', '교과영역', '과목번호', '과목명', '분반', '교수명',
                        '개설학과', '시간/학점(설계)', '수강인원', '여석', '강의시간(강의실)', '수강대상'])
                    }
                ]
                *문학과 예술(융합-인문): []
                *역사와철학(융합-인문): []
                *정보와기술(융합-자연): []
                *창의성과의사소통능력(핵심-창의): []
                *세계의언어(핵심-창의): []
                *세계의문화와국제관계(핵심-창의): []
                *인간과사회(융합-사회): []
                *정치와경제(융합-사회): []
                *자연과학과수리(융합-자연): []
                *생활과건강(실용-생활): []
                *학문과진로탐색(실용-생활): []
                *인성과리더쉽(핵심-창의): []
                숭실품성(인성-종교가치인성교육): []
                숭실품성(인성-가치관및윤리교육): []
                숭실품성(인성-공동체인성교육): []
                숭실품성(리더십-통일리더십): []
                숭실품성(리더십-리더십이론및실천): []
                기초역량(사고력-논리및비판적사고): []
                기초역량(사고력-창의및융합적사고): []
                기초역량(사고력-수리적사고): []
                기초역량(한국어의사소통-읽기와쓰기): []
                기초역량(한국어의사소통-의사소통): []
                (기초역량-국제어문)영어: []
                기초역량(국제어문-국제어): []
                기초역량(국제어문-고전어문 ): []
                기초역량(과학정보기술-과학): []
                기초역량(과학정보기술-정보기술): []
                균형교양(인문학-문학/어학/예술): []
                균형교양(인문학-역사): []
                균형교양(인문학-철학/사상): []
                균형교양(사회과학-사회/정치/경제): []
                균형교양(사회과학-문화및문명): []
                균형교양(자연과학-자연과학): []
                실용교양(개인과가족생활): []
                실용교양(경제경영): []
                실용교양(공공생활): []
                실용교양(기술생활): []
                실용교양(자기개발과진로탐색)
            }
        },
        year: {
            'semester': {
                'section': [
                    {
                        dict_keys(['계획', '이수구분(주전공)', '이수구분(다전공)',
                        '공학인증', '교과영역', '과목번호', '과목명', '분반', '교수명',
                        '개설학과', '시간/학점(설계)', '수강인원', '여석', '강의시간(강의실)', '수강대상'])
                    }
                ]
            }
        }
    }
    """
    ret = {year: {} for year in year_range}
    saint = Saint()
    saint.select_course_section('교양선택')

    # is this necessary job?
    saint.select_year('2017')
    saint.select_semester('2 학기')

    def __get_whole_course(year, semester):
        saint.select_year(year)
        saint.select_semester(semester)
        selective_map = saint.get_selective_liberal_map()
        course_map = {course_name: {} for course_name in selective_map}

        pbar = tqdm(selective_map, disable=silent)
        for course_name in pbar:
            pbar.set_description("Processing {:8s}".format(course_name))
            if course_name != '':
                course_map[course_name] = saint.select_on_selective_liberal(course_name)

        return course_map

    year_bar = tqdm(year_range, disable=silent)
    for year in year_bar:
        year_bar.set_description("Year: {:4s}".format(year))
        semester_bar = tqdm(semesters, disable=silent)
        for semester in semester_bar:
            semester_bar.set_description("semester: {:6s}".format(semester))
            course_bunch = __get_whole_course(year, semester)
            ret[year][semester] = course_bunch

    return ret


def _cyber(year_range=[], semesters=[], silent=False):
    """
    TODO:
    시간나면 만들기
    :param year_range:
    :param semesters:
    :return:
    """


def login(user_id, password=None):
    """
    log in saint.ssu.ac.kr
    :param user_id:  student id
    :param password: saint password
    :return:
    """
    if password is None:
        import getpass
        password = getpass.getpass("PASSWORD for {}: ".format(user_id))
    else:
        password = password

    saint = Saint()
    saint.login(user_id, password)
    return saint
