```python
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
    course_map = {course_name: {} for course_name in selective_map}

    for course_name in selective_map:
        if course_name != '':
            course_map[course_name] = saint.select_on_selective_liberal(course_name)

    return course_map


for year in range(2017, 2008, -1):
    for semester in ['1 학기', '여름학기', '2 학기', '겨울학기']:
        course_bunch = get_whole_course(year, semester)
        utils.save_json('./pickles/교양선택json/', '{}-{}-교양선택.json'.format(year, semester), course_bunch)

```