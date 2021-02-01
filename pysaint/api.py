"""
    End User를 위한 간단한 api


"""

from .constants import Line
from .saint import Saint
import copy
from tqdm import tqdm
from datetime import datetime

def get(course_type, year_range, semesters, line=Line.FIVE_HUNDRED, **kwargs):
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

        >>> res = pysaint.get('전공', ['2018'], ['2 학기'], line=200)
        >>> print(res)

    :param course_type:
    :type course_type: str
    example )
            '교양필수'
            '전공'
            '연계전공'
            '교양선택'
            '교직'
            '채플'
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

    :param line:
        :type line: int
        example )
                10
                20
                50
                100
                200
                500

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

    if not Line.has_value(line):
        raise ValueError("get() got wrong arguments line: {}\n"
                         "line should be one of {}".format(line, Line.list()))

    reformed_year_range = []
    current_year = datetime.now().year
    for year in year_range:
        if 2000 < int(year) <= current_year:
            pass
        else:
            raise ValueError("get() got wrong arguments year_range: {}\n"
                             "expected to be in year range(2000, 2021) but got {}".format(year_range, int(year)))
        reformed_year_range.append("{}".format(year))

    if course_type == '교양필수':
        return _liberal_arts(year_range=reformed_year_range, semesters=semesters, line=line, **kwargs)
    elif course_type == '전공':
        return _major(year_range=reformed_year_range, semesters=semesters, line=line,**kwargs)
    elif course_type == '교양선택':
        return _selective_liberal(year_range=reformed_year_range, semesters=semesters, line=line, **kwargs)
    elif course_type == '연계전공':
        return _related_major(year_range=reformed_year_range, semesters=semesters, line=line, **kwargs)
    elif course_type == '융합전공':
        return _fusion_major(year_range=reformed_year_range, semesters=semesters, line=line, **kwargs)
    elif course_type == '교직':
        return _teaching(year_range=reformed_year_range, semesters=semesters, line=line, **kwargs)
    elif course_type == '채플':
        return _chapel(year_range=reformed_year_range, semesters=semesters, line=line, **kwargs)
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


def _liberal_arts(year_range=[], semesters=[], line=int(Line.FIVE_HUNDRED), silent=False):
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

    :param line:
        :type line: int
        example )
                10
                20
                50
                100
                200
                500

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

    def __get_whole_course(year, semester, _line=line):

        saint.select_year(year)
        saint.select_semester(semester)
        saint.select_line(_line)
        liberal_map = saint.get_liberal_arts_map()
        course_map = {name: [] for name in liberal_map}

        pbar = tqdm(liberal_map, disable=silent)
        for course_name in pbar:
            pbar.set_description("Processing {:8s}".format(course_name))
            course_map[course_name] = saint.select_on_liberal_arts(course_name)

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


def _major(year_range=[], semesters=[], line=Line.FIVE_HUNDRED, silent=False):
    """
    전공 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :type year_range: list or tuple
    :param semesters:
    :type semesters: list or tuple
    :param line:
    :type line: int
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

    def __get_whole_course(year, semester, _line=line):
        saint.select_year(year)
        saint.select_semester(semester)
        saint.select_line(_line)
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


def _selective_liberal(year_range=[], semesters=[], line=Line.FIVE_HUNDRED, silent=False):
    """
    교양선택 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :param line:
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

    def __get_whole_course(year, semester, _line=line):
        saint.select_year(year)
        saint.select_semester(semester)
        saint.select_line(_line)
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

def _related_major(year_range=[], semesters=[], line=Line.FIVE_HUNDRED, silent=False):
    """
    교양선택 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :param line:
    :return: dict

    {
        2017: {
            '1 학기': {
                "중국어경제국제통상연계전공": [
                    {
                        "계획": " ",
                        "이수구분(주전공)": "전선-경제",
                        "이수구분(다전공)": "복선-경제/부선-경제/연계2-벤처자본경제학/연계2-일본어경제통상/연계2-중국어경제통상",
                        "공학인증": " ",
                        "교과영역": " ",
                        "과목번호": "2150191901",
                        "과목명": "공공경제학(실시간화상강의) (온라인)",
                        "분반": " ",
                        "교수명": "우진희\n우진희",
                        "개설학과": "경제학과",
                        "시간/학점(설계)": "3.00 /3.0 (0 )",
                        "수강인원": "0",
                        "여석": "35",
                        "강의시간(강의실)": "월 15:00-16:15 (-우진희)\n수 13:30-14:45 (숭덕경상관 02109-우진희)",
                        "수강대상": "3학년 경제,벤처자본경제학,일본어경제통상,중국어경제통상"
                    }
                ]
                일본어경제국제통상연계전공: []
                금융공학·보험계리연계전공: []
                영어·중국어연계전공: []
                PreMed연계전공: []
                벤처자본경제학연계전공: []
                보험계리·리스크연계전공: []
                융합창업연계: []
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
    saint.select_course_section('연계전공')

    # is this necessary job?
    saint.select_year('2017')
    saint.select_semester('2 학기')

    def __get_whole_course(year, semester, _line=line):
        saint.select_year(year)
        saint.select_semester(semester)
        saint.select_line(_line)
        related_major_map = saint.get_related_major_map()
        course_map = {course_name: {} for course_name in related_major_map}

        pbar = tqdm(related_major_map, disable=silent)
        for course_name in pbar:
            pbar.set_description("Processing {:8s}".format(course_name))
            if course_name != '':
                course_map[course_name] = saint.select_on_related_major(course_name)

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

def _fusion_major(year_range=[], semesters=[], line=Line.FIVE_HUNDRED, silent=False):
    """
    융합전공 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :param line:
    :return: dict

    {
        2021: {
            '1 학기': {
                "빅데이터융합": [
                    {
                        "계획": " ",
                        "이수구분(주전공)": "전필-소프트",
                        "이수구분(다전공)": "복필-소프트/융선-빅데이터융합",
                        "공학인증": "공학주제-소프트공인증/인필-소프트공인증",
                        "교과영역": " ",
                        "과목번호": "2150013201",
                        "과목명": "데이터베이스(실시간화상+사전녹화강의) (온라인) ( 가반 )",
                        "분반": " ",
                        "교수명": " ",
                        "개설학과": "소프트웨어학부",
                        "시간/학점(설계)": "3.00 /3.0",
                        "수강인원": "0",
                        "여석": "40",
                        "강의시간(강의실)": "월 15:00-16:15 (-)",
                        "수강대상": "3학년 소프트,빅데이터융합"
                    }
                ]
                빅데이터컴퓨팅융합: []
                스마트소재/제품융합: []
                스마트이동체융합: []
                양자나노융합: []
                에너지공학융합: []
                통일외교및개발협력융합: []
                스마트자동차융합: []
                정보보호융합: []
                ICT유통물류융합: []
                문화서비스산업융합: []
                스포츠마케팅융합: []
                사물인터넷시스템융합: []
                과학철학융합: []
                인간및사회통섭융합: []
                헬스케어빅데이터융합: []
                디자인플래닝융합: []
                사회적기업과사회혁신융합: []
                스포츠매니지먼트융합: []
                IT스타트업엑셀러레이터융합: []
                AI로봇융합: []
                뉴미디어콘텐츠융합: []
                문화콘텐츠비즈니스융합: [],
                주거복지도시행정융합: [],
                메카트로닉스공학융합: [],
                프레임/사회이슈기획융합: [],
                사회공동체혁신융합: [],
                네러티브디지털아트융합: [],
                사회분석데이터마케팅융합: [],
                패션미디어마케팅융합: [],
                국제도시계획⋅행정융합: [],
                토탈디자인브랜딩융합: [],
                AI-인지언어융합: [],
                뉴미디어마케팅융합: [],
                동아시아경제통상융합: [
                AI모빌리티융합: [],
                스마트안전보건환경융합: [],
                데이터마케팅융합: [],
                지속가능디자인융합: []
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
    saint.select_course_section('융합전공')

    # is this necessary job?
    saint.select_year('2017')
    saint.select_semester('2 학기')

    def __get_whole_course(year, semester, _line=line):
        saint.select_year(year)
        saint.select_semester(semester)
        saint.select_line(_line)
        fusion_major_map = saint.get_fusion_major_map()
        course_map = {course_name: {} for course_name in fusion_major_map}

        pbar = tqdm(fusion_major_map, disable=silent)
        for course_name in pbar:
            pbar.set_description("Processing {:8s}".format(course_name))
            if course_name != '':
                course_map[course_name] = saint.select_on_fusion_major(course_name)

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

def _teaching(year_range=[], semesters=[], line=Line.FIVE_HUNDRED, silent=False):
    """
    교직 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :param line:
    :return: dict

    {
        2021: {
            '1 학기': {
                "교직": [
                    {
                        "계획": " ",
                        "이수구분(주전공)": "교직",
                        "이수구분(다전공)": " ",
                        "공학인증": " ",
                        "교과영역": "교직이론영역",
                        "과목번호": "5011868701",
                        "과목명": "교육과정(실시간화상강의) (온라인)",
                        "분반": " ",
                        "교수명": "조호제",
                        "개설학과": "교직팀",
                        "시간/학점(설계)": "2.00 /2.0 (0 )",
                        "수강인원": "0",
                        "여석": "30",
                        "강의시간(강의실)": "금 18:00-19:50 (-조호제)",
                        "수강대상": "전체"
                    }
                ]
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
    saint.select_course_section('교직')

    # is this necessary job?
    saint.select_year('2017')
    saint.select_semester('2 학기')

    def __get_whole_course(year, semester, _line=line):
        saint.select_year(year)
        saint.select_semester(semester)
        saint.select_line(_line)
        teaching_map = ['교직']
        course_map = {course_name: {} for course_name in teaching_map}

        pbar = tqdm(teaching_map, disable=silent)
        for course_name in pbar:
            pbar.set_description("Processing {:8s}".format(course_name))
            if course_name != '':
                course_map[course_name] = saint.select_on_teaching()

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

def _chapel(year_range=[], semesters=[], line=Line.FIVE_HUNDRED, silent=False):
    """
    채플 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :param line:
    :return: dict

    {
        2021: {
            '1 학기': {
                "교수와함께하는채플": [
                    {
                        "계획": " ",
                        "이수구분(주전공)": "채플",
                        "이수구분(다전공)": " ",
                        "공학인증": " ",
                        "교과영역": "채플과목",
                        "과목번호": "2150051501",
                        "과목명": "교수와함께하는채플",
                        "분반": " ",
                        "교수명": "강아람",
                        "개설학과": "학원선교팀",
                        "시간/학점(설계)": "1.00 /0.5",
                        "수강인원": "0",
                        "여석": "15",
                        "강의시간(강의실)": "화 15:00-15:50 (진리관 11111-강아람)",
                        "수강대상": "전체"
                    }
                ],
                "CHAPEL": []
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
    saint.select_course_section('채플')

    # is this necessary job?
    saint.select_year('2017')
    saint.select_semester('2 학기')

    def __get_whole_course(year, semester, _line=line):
        saint.select_year(year)
        saint.select_semester(semester)
        saint.select_line(_line)
        chapel_map = saint.get_chapel_map()
        course_map = {course_name: {} for course_name in chapel_map}

        pbar = tqdm(chapel_map, disable=silent)
        for course_name in pbar:
            pbar.set_description("Processing {:8s}".format(course_name))
            if course_name != '':
                course_map[course_name] = saint.select_on_chapel(course_name)

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
