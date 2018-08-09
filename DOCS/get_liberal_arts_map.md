```python
from pysaint import Saint

saint = Saint()
saint.select_course_section('교양필수')
saint.select_year('2017')
saint.select_semester('2 학기')
map = saint.get_liberal_arts_map()
print(map)
>> {'1학년': ['현대인과성서세미나',
  '문예융합세미나',
  '‘C&G.C’ Seminar',
  '컴퓨팅적사고',
  '영어1',
  '영어2',
  '현대인과성서',
  '창의적사고와글쓰기',
  '영어2(고급)',
  '한반도평화와통일',
  '창의적사고와독서토론'],
 '2학년': ['숭실인의역량과진로탐색2'],
 '3학년': [''],
 '4학년': [''],
 '5학년': [''],
 '전체학년': ['CHAPEL']}


# Saint.select_course_section을 다시 호출하지 않아도 된다.
saint.select_year('2017')
saint.select_semester('1 학기')
map = saint.get_liberal_arts_map()
print(map)
>> {'1학년': ['현대인과성서세미나',
  '문예융합세미나',
  '‘C&G.C’ Seminar',
  '컴퓨팅적사고',
  '영어1',
  '영어2',
  '현대인과성서',
  '창의적사고와글쓰기',
  '영어2(고급)',
  '한반도평화와통일',
  '창의적사고와독서토론'],
 '2학년': ['숭실인의역량과진로탐색2'],
 '3학년': [''],
 '4학년': [''],
 '5학년': [''],
 '전체학년': ['CHAPEL']}
```
