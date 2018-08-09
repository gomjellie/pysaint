# pysaint

## setup

```sh
python ./setup.py install
```
## Usage

```python
from pysaint import Saint
from pysaint import utils
import copy

saint = Saint()

def get_whole_course(year, semester):
    print('{} {}'.format(year, semester))
    saint.select_year('2017')
    saint.select_semester('1 학기')
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


for year in range(2016, 2011, -1):
    for semester in ['1 학기', '여름학기', '2 학기', '겨울학기']:
        course_bunch = get_whole_course(year, semester)
        utils.save_pickle('./pickles', '{}-{}-전공'.format(year, semester), course_bunch)


```
