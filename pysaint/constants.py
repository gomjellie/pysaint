SOURCE_URL = "https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/zcmw2100?sap-language=KO"
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
    'Referer': 'https://saint.ssu.ac.kr/irj/portal',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)" +
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

SESSION_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'ecc.ssu.ac.kr',
    'Origin': 'https://saint.ssu.ac.kr',
    'Referer': 'https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/zcmw2100?sap-language=KO',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    'Upgrade-Insecure-Requests': '1',
    'X-XHR-Logon': 'accept',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " +
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
}

SESSION_HEADERS_GRADE = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR',
    'Authorization': 'Basic MjAxNTAzMTg6c29vbmdzaWxAUzE=',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'ecc.ssu.ac.kr',
    'Origin': 'https://ecc.ssu.ac.kr',
    'Referer': 'https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/ZCMB3W0017',
    # 'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    # 'sec-ch-ua-mobile': '?0',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    # 'Upgrade-Insecure-Requests': '1',
    'X-XHR-Logon': 'accept',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
}

GRADE_POST_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Authorization': 'Basic MjAxNTAzMTg6c29vbmdzaWxAUzE=',
    'Accept-Language': 'en-us',
    'Accept-Encoding': 'gzip, deflate, br',
    # 'Host': 'ecc.ssu.ac.kr',
    'Origin': 'https://ecc.ssu.ac.kr',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
    # 'Referer': 'https://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/ZCMB3W0017?sap-language=KO',
    'Connection': 'keep-alive',
    # 'Cookie': 'MYSAPSSO2=AjQxMDIBABgAMgAwADEANQAwADMAMQA4ACAAIAAgACACAAYAMQAwADADABAAUwBTAFAAIAAgACAAIAAgBAAYADIAMAAyADAAMQAyADIAMgAxADUAMQA1BQAEAAAACAYAAgBYCQACADP%2fAPQwgfEGCSqGSIb3DQEHAqCB4zCB4AIBATELMAkGBSsOAwIaBQAwCwYJKoZIhvcNAQcBMYHAMIG9AgEBMBMwDjEMMAoGA1UEAxMDU1NQAgEAMAkGBSsOAwIaBQCgXTAYBgkqhkiG9w0BCQMxCwYJKoZIhvcNAQcBMBwGCSqGSIb3DQEJBTEPFw0yMDEyMjIxNTE1MTNaMCMGCSqGSIb3DQEJBDEWBBQsOLWeWwq81ipvgaPBUTwCvChdhjAJBgcqhkjOOAQDBC4wLAIUG3uCGqmTxlHaUG9EQCuC%216FzYTUCFCuDoWZDWf%21kYhK0vhkt7%2fQKV%2fqh; SAP_SESSIONID_SSP_100=NjiqVlEYVhYHcxmFSWhu4n1WbkJEaBHroXhpNxfuS6c%3d; SAPWP_active=1; sap-usercontext=sap-language=KO&sap-client=100',
    # 'X-Requested-With': 'XMLHttpRequest',
    # 'X-XHR-Logon': 'accept',
}

GRADE_GET_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'ecc.ssu.ac.kr',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
    # 'Authorization': 'Basic MjAxNTAzMTg6c29vbmdzaWxAUzE=',
    'Accept-Language': 'en-us',
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
