SOURCE_URL = "http://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/zcmw2100?sap-language=KO"
ECC_URL = "http://ecc.ssu.ac.kr"
SAINT_URL = "https://saint.ssu.ac.kr"
PORTAL_URL = "https://saint.ssu.ac.kr/irj/portal"
POPUP_URL = "https://saint.ssu.ac.kr/ssu_logon/jsp/popupCheck.jsp"

REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'saint.ssu.ac.kr',
    'Origin': 'https://saint.ssu.ac.kr',
    'Referer': 'http://saint.ssu.ac.kr/irj/portal',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

SESSION_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'saint.ssu.ac.kr',
    'Origin': 'https://saint.ssu.ac.kr',
    'Referer': 'https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/zcmw2100?sap-language=KO',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XHR-Logon': 'accept',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

GRADE_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'saint.ssu.ac.kr',
    'Origin': 'https://saint.ssu.ac.kr',
    'Referer': 'https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/ZCMB3W0017',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XHR-Logon': 'accept',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

GRADE_POST_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Cache-Control': 'max-age=0',
    # 'Authorization': 'Basic MjAxNTAzMTg6c29vbmdzaWxAUzE=',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'ecc.ssu.ac.kr',
    'Origin': 'http://saint.ssu.ac.kr',
    'Referer': 'http://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/ZCMB3W0017?sap-language=KO',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XHR-Logon': 'accept',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

GRADE_GET_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'max-age=0',
    'Host': 'ecc.ssu.ac.kr',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept-Language': 'ko-KR',
    'Connection': 'keep-alive'
}

class Line:
    TEN = 10
    TWENTY = 20
    FIFTY = 50
    HUNDRED = 100
    TWO_HUNDRED = 200
    FIVE_HUNDRED = 500

    @classmethod
    def list(cls):
        members = [getattr(Line, attr) for attr in dir(Line) if not callable(getattr(Line, attr)) and not attr.startswith("__")]
        return sorted(members)
    
    @classmethod
    def has_value(cls, val):
        return val in cls.list()
