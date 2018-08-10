"""
    End User를 위한 간단한 api


"""

from .saint import Saint
import copy


def get(course_type, year_range, semesters, **kwargs):
    """

    :param course_type:
    :type course_type: str
    example )
            '교양필수'
            '전공'
            '교양선택'
    :param year_range:
    :type year_range: list or tuple
    :param semesters:
    :type semesters: list or tuple
    :return:
    """
    if course_type == '교양필수':
        return _liberal_arts(year_range=year_range, semesters=semesters, **kwargs)
    elif course_type == '전공':
        pass
    elif course_type == '교양선택':
        pass
    else:
        raise Exception("Unexpected param course_type {} \n".format(
            course_type
        ))


def _liberal_arts(year_range=[], semesters=[], **kwargs):
    """
    TODO: validate parameters!
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

    def _get_whole_course(year, semester):
        print('{} {}'.format(year, semester))
        saint.select_year(year)
        saint.select_semester(semester)
        liberal_map = saint.get_liberal_arts_map()
        course_map = copy.deepcopy(liberal_map)

        for grade in liberal_map:
            course_map[grade] = {course_name: {} for course_name in liberal_map[grade]}

        for grade in liberal_map:
            for course_name in liberal_map[grade]:
                if course_name != '':
                    course_map[grade][course_name] = saint.select_on_liberal_arts(grade, course_name)

        return course_map

    for year in year_range:
        for semester in semesters:
            course_bunch = _get_whole_course(year, semester)
            ret[year][semester] = course_bunch

    return ret


def _major(year_range=[], semesters=[], **kwargs):
    """
    전공 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :return:
    """

    ret = {year: {} for year in year_range}
    saint = Saint()

    def get_whole_course(year, semester):
        print('{} {}'.format(year, semester))
        saint.select_year(year)
        saint.select_semester(semester)
        major_map = saint.get_major_map()
        course_map = copy.deepcopy(major_map)

        for college in major_map:
            for faculty in major_map[college]:
                course_map[college][faculty] = {key: [] for key in major_map[college][faculty]}

        for college in major_map:
            for faculty in major_map[college]:
                for major in major_map[college][faculty]:
                    print('{} {} {}'.format(college, faculty, major))
                    course_map[college][faculty][major] = saint.select_on_major(college, faculty, major)

        return course_map

    for year in year_range:
        for semester in semesters:
            course_bunch = get_whole_course(year, semester)
            ret[year][semester] = course_bunch

    return ret


def selective_liberal(year_range=[], semesters=[], **kwargs):
    """
    교양선택 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :return:
    """


def cyber(year_range=[], semesters=[], **kwargs):
    """
    TODO:
    시간나면 만들기
    :param year_range:
    :param semesters:
    :return:
    """
