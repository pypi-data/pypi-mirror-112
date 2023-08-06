__all__ = ('Session', 'session')



import functools
import pickle
import requests

from .others import Faker as F
from ..conf import pickle_path



class Session:
    '''Bilibili Session model

    API:
        - value
            - session
            - browser
            - requests
        - property
            - is_login
        - function
            - set_headers(headers: dict)
            - set_cookies(cookies: dict)
            - set_cookies_from_selenium(webdriver: selenium.webdriver.Remote)
            - set_user_agent(user_agent: dict)
            - login_by_selenium(name: str)
            + login_by_password(username: str, password: str)
        - decorator
            - required_login(func)
    '''

    def __init__(self, login_by='selenium'):
        self.requests = requests
        self.session = requests.Session()
        self.session.headers.update({
            'host': 'api.bilibili.com',
            'referer': 'https://www.bilibili.com',
            'user-agent': F.user_agent(),
        })
        self.browser = None
        self._login = False
        self._login_by = getattr(self, f'login_by_{login_by}')


    @property
    def is_login(self):
        return self._login


    def dump(self, path=pickle_path):
        data = dict(
            headers=self.session.headers,
            cookies=self.session.cookies,
            login=self._login,
        )
        with open(path, 'wb') as f:
            pickle.dump(data, f)


    def load(self, path=pickle_path):
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self._login = data['login']
        self.session.headers = data['headers']
        self.session.cookies = data['cookies']


    def set_headers(self, headers):
        '''
        Argument:
            - headers: dict
        '''
        self.session.headers.update(headers)


    def set_cookies(self, cookies):
        '''
        Argument:
            - cookies: dict
        '''
        self.session.cookies.update(cookies)


    def set_cookies_from_selenium(self, webdriver):
        '''Set cookies from `selenium`
        '''
        cookies = webdriver.get_cookies()
        self.set_cookies({item['name']: item['value'] for item in cookies})


    def set_user_agent(self, user_agent=None):
        '''
        Argument:
            - user_agent: str
        '''
        self.set_headers({'user-agent': (user_agent or F.user_agent())})


    def login_by_selenium(self, name='Firefox'):
        '''
        Argument:
            - name: str, selenium.webdriver.`name`
        '''
        from selenium import webdriver

        self.browser = getattr(webdriver, name)()
        self.browser.get('https://passport.bilibili.com/login')
        input('Please login in >>> ')
        self.set_cookies_from_selenium(self.browser)
        self._login = True


    def login_by_password(self, username, password):
        '''
        References:
            - https://github.com/Hsury/Bilibili-Toolkit
            - https://github.com/apachecn/BiliDriveEx
        '''
        raise NotImplementedError


    def required_login(self, *outer_args, **outer_kwargs):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self._login:
                    self._login_by(*outer_args, **outer_kwargs)
                return func(*args, **kwargs)
            return wrapper
        return decorator



session = Session()
