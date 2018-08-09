"""
    세인트에 있는 전공 과목들의 트리 구조를 가져와서 json 으로 저장합니다.
"""
from pysaint import Saint
from pysaint import utils

saint = Saint()


def get_whole_course(year, semester):
    print('{} {}'.format(year, semester))
    saint.select_year(year)
    saint.select_semester(semester)
    major_map = saint.get_major_map()

    return major_map


for year in range(2017, 2008, -1):
    for semester in ['1 학기', '여름학기', '2 학기', '겨울학기']:
        course_bunch = get_whole_course(year, semester)
        utils.save_json('./json/maps/전공/', '{}-{}-전공.json'.format(year, semester), course_bunch)
