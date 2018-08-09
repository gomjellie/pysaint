"""
    End User를 위한 간단한 api


"""

from pysaint import Saint
import copy
from collections import defaultdict


def liberal_arts(year_range=[], semesters=[]):
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


def major(year_range=[], semesters=[]):
    """
    전공 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :return:
    """


def selective_liberal(year_range=[], semesters=[]):
    """
    교양선택 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :return:
    """


def cyber(year_range=[], semesters=[]):
    """
    TODO:
    시간나면 만들기
    :param year_range:
    :param semesters:
    :return:
    """
