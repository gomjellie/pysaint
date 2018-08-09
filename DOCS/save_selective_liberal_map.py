"""
    세인트에서 교양선택의 트리 구조를 가져와서 json 으로 저장합니다.
"""
from pysaint import Saint
from pysaint import utils

saint = Saint()
saint.select_course_section('교양선택')
saint.select_year('2017')
saint.select_semester('2 학기')


def get_whole_course(year, semester):
    print('{} {}'.format(year, semester))
    saint.select_year(year)
    saint.select_semester(semester)
    selective_map = saint.get_selective_liberal_map()

    return selective_map


for year in range(2017, 2008, -1):
    for semester in ['1 학기', '여름학기', '2 학기', '겨울학기']:
        course_bunch = get_whole_course(year, semester)
        utils.save_json('./json/maps/교양선택/', '{}-{}-교양선택.json'.format(year, semester), course_bunch)

