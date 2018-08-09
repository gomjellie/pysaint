```python
from pysaint import Saint
from pysaint import utils
import copy

saint = Saint()
saint.select_course_section('교양필수')

def get_whole_course(year, semester):
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


for year in range(2017, 2011, -1):
    for semester in ['1 학기', '여름학기', '2 학기', '겨울학기']:
        course_bunch = get_whole_course(year, semester)
        utils.save_json('./pickles/교양필수json/', '{}-{}-교양필수.json'.format(year, semester), course_bunch)
        utils.save_pickle('./pickles', '{}-{}-교양필수'.format(year, semester), course_bunch)

```