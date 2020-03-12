from random import choice
import requests


class Utils:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"]
    MOBILE_USER_AGENTS = []

    @staticmethod
    def fetch(url, headers=None, cookies=None):
        if headers is None:
            user_agent = choice(Utils.USER_AGENTS)
            headers = {'User-Agent': user_agent}
        with requests.get(url, headers=headers, cookies=cookies) as response:
            response.encoding = response.apparent_encoding
            # TODO: refactor, cookies
            return response.content
            # return response.text
        return ""


url = 'https://httpbin.org/user-agent'


def main():
    print(Utils.fetch("http://httpbin.org/headers"))


if __name__ == '__main__':
    main()
