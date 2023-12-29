import requests

class RequestMethods:
    def __init__(self, url_oc) -> None:
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'
        }
        self.sess = requests.Session()
        self.url_oc = url_oc
        self.cookies = {}

    def get_data(self, url):
        self.set_cookie()
        response = self.sess.get(url, headers=self.headers, cookies=self.cookies, timeout=5)

        if(response.status_code==401):
            self.set_cookie()
            response = self.sess.get(url, headers=self.headers, cookies=self.cookies, timeout=5)
        if response.status_code == 200:
            return response.text
        return f"Getting this: {response}."

    def set_cookie(self):
        request = self.sess.get(self.url_oc, headers=self.headers, timeout=5)
        self.cookies = dict(request.cookies)