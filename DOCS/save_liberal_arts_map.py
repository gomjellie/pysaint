"""
    세인트에 있는 교양필수 과목들의 트리 구조를 가져와서 json 으로 저장합니다.
"""
from pysaint import Saint
from pysaint import utils

saint = Saint()
saint.select_course_section('교양필수')


def get_whole_course(year, semester):
    print('{} {}'.format(year, semester))
    saint.select_year(year)
    saint.select_semester(semester)
    liberal_map = saint.get_liberal_arts_map()

    return liberal_map


for year in range(2017, 2008, -1):
    for semester in ['1 학기', '여름학기', '2 학기', '겨울학기']:
        course_bunch = get_whole_course(year, semester)
        utils.save_json('./json/maps/교양필수/', '{}-{}-교양필수.json'.format(year, semester), course_bunch)

