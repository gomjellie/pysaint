# pysaint

saint.ssu.ac.kr 에서 수강신청 과목정보를 실시간으로 가져오는 라이브러리 입니다.

## setup (for library developer)

```sh
python ./setup.py build
python ./setup.py install
```

## setup (for end user)
```sh
pip install pysaint
```
## Usage

```python
import pysaint

res = pysaint.get('전공', ['2018'], ['2 학기'])
print(res)

res = pysaint.get('교양필수', range(2015, 2017), ('1 학기', '여름학기', '2 학기', '겨울학기'))
print(res)

res = pysaint.get('교양선택', (2016, ), ('1 학기', ))
print(res)

pysaint.save_json('./json/', '{}-{}-전공'.format('2016', '1 학기'), res)


```
