

```python

import pysaint

res = pysaint.get('전공', ['2018'], ['2 학기'])
print(res)


res = pysaint.get('교양필수', range(2015, 2017), ['1 학기', '여름학기', '2 학기', '겨울학기'])
print(res)


res = pysaint.get('교양선택', (2016, 2017, 2018), ('1 학기', ))
print(res)

```