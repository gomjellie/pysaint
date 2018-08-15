# pysaint

saint.ssu.ac.kr 에서 수강신청 과목정보를 실시간으로 가져오는 라이브러리 입니다.

## setup (for end user)
```sh
pip install pysaint
```

## Usage

```python
import pysaint

res = pysaint.get('전공', '2018', '2 학기', silent=True)
print(res)

>>
{
    "2018": {
        "2 학기": {
            "인문대학": {
                "기독교학과": {
                    "기독교학과": [
                        {
                            "계획": " ",
                            "이수구분(주전공)": "전기-기독교",
                            "이수구분(다전공)": "복필-기독교/부필-기독교",
                            "공학인증": " ",
                            "교과영역": " ",
                            "과목번호": "2150655801",
                            "과목명": "기독교사회학개론",
                            "분반": " ",
                            "교수명": "이철\n이철",
                            "개설학과": "기독교학과",
                            "시간/학점(설계)": "3.00 /3",
                            "수강인원": "0",
                            "여석": "50",
                            "강의시간(강의실)": "수 10:30-11:45 (진리관 11307-이철)\n목 12:00-13:15 (조만식기념관 12202-이철)",
                            "수강대상": "1학년 기독교"
                        },
                        {
                            "계획": " ",
                            "이수구분(주전공)": "전기-기독교",
                            "이수구분(다전공)": "복필-기독교",
                            "공학인증": " ",
                            "교과영역": " ",
                            "과목번호": "2150655901",
                            "과목명": "기독교상담심리학",
                            "분반": " ",
                            "교수명": "박승민\n박승민",
                            "개설학과": "기독교학과",
                            "시간/학점(설계)": "3.00 /3",
                            "수강인원": "0",
                            "여석": "60",
                            "강의시간(강의실)": "화 12:00-13:15 (조만식기념관 12328-박승민)\n목 10:30-11:45 (조만식기념관 12202-박승민)",
                            "수강대상": "1학년 기독교"
                        },
                        {
                            "계획": " ",
                            "이수구분(주전공)": "전기-기독교",
                            "이수구분(다전공)": "복필-기독교/부필-기독교",
                            "공학인증": " ",
                            "교과영역": " ",
                            "과목번호": "2150517001",
                            "과목명": "기독교학서론",
                            "분반": " ",
                            "교수명": "권연경\n권연경",
                            "개설학과": "기독교학과",
                            "시간/학점(설계)": "3.00 /3 (0 )",
                            "수강인원": "0",
                            "여석": "60",
                            "강의시간(강의실)": "수 09:00-10:15 (조만식기념관 12202-권연경)\n금 12:00-13:15 (조만식기념관 12310-권연경)",
                            "수강대상": "1학년 기독교"
                        },
                        ...


res = pysaint.get('교양필수', range(2015, 2017), ('1 학기', '여름학기', '2 학기', '겨울학기'))
print(res)
>>>
{
  "2015": {
    "1 학기": {
      "전체학년": {
        "CHAPEL": [
          {
            "계획": " ",
            "이수구분(주전공)": "교필",
            "이수구분(다전공)": " ",
            "공학인증": " ",
            "교과영역": "채플과목",
            "과목번호": "2150101513",
            "과목명": "채플",
            "분반": " ",
            "교수명": " ",
            "개설학과": "베어드학부대학 행정팀",
            "시간/학점(설계)": "1.00 /0 (0 )",
            "수강인원": "187",
            "여석": "812",
            "강의시간(강의실)": "토 07:00-07:50 (형남공학관 050115-)",
            "수강대상": "전체학년 금융경제 ,국제무역 ,혁신경영학과(계약학과) ,벤처경영학과(계약학과)"
          },
          {
            "계획": " ",
            "이수구분(주전공)": "교필",
            "이수구분(다전공)": " ",
            "공학인증": " ",
            "교과영역": "채플과목",
            "과목번호": "2150101512",
            "과목명": "채플(공통채플:기독인채플)",
            "분반": " ",
            "교수명": " ",
            "개설학과": "베어드학부대학 행정팀",
            "시간/학점(설계)": "1.00 /0 (0 )",
            "수강인원": "117",
            "여석": "0",
            "강의시간(강의실)": "수 15:00-15:50 (-)",
            "수강대상": "전체"
          },
          ...

res = pysaint.get('교양선택', (2016, ), ('1 학기', ), silent=False)
print(res)
{
  "2016": {
    "1 학기": {
      "전체": [
        {
          "계획": " ",
          "이수구분(주전공)": "교선",
          "이수구분(다전공)": " ",
          "공학인증": " ",
          "교과영역": "균형교양(자연과학-자연과학)\n*자연과학과수리(융합-자연)",
          "과목번호": "2150116601",
          "과목명": "과학사",
          "분반": " ",
          "교수명": "이권재",
          "개설학과": "물리학과",
          "시간/학점(설계)": "3.00 /3 (0 )",
          "수강인원": "32",
          "여석": "18",
          "강의시간(강의실)": "월 수 16:30-17:45 (조만식기념관 12525-이권재)",
          "수강대상": "전체"
        },
        {
          "계획": " ",
          "이수구분(주전공)": "교선",
          "이수구분(다전공)": " ",
          "공학인증": " ",
          "교과영역": "균형교양(사회과학-사회/정치/경제)\n*세계의문화와국제관계(핵심-창의)",
          "과목번호": "2150121901",
          "과목명": "국제관계의이해",
          "분반": " ",
          "교수명": "이한규",
          "개설학과": "정치외교학과",
          "시간/학점(설계)": "3.00 /3 (0 )",
          "수강인원": "57",
          "여석": "3",
          "강의시간(강의실)": "월 수 15:00-16:15 (미래관 20403-이한규)",
          "수강대상": "전체"
        },
        ...

# freeze as json file format
pysaint.save_json('./json/', '{}-{}-전공'.format('2016', '1 학기'), res)


```
