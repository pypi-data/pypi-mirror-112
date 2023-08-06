import os
import sys

__version__ = '0.1.20.dev1'

def login(api_token=None):
    if api_token is None and 'finlab_id_token' not in os.environ:
        try:
            from IPython.display import IFrame, display, clear_output
            iframe = IFrame('https://ai.finlab.tw/api_token/', width=620, height=300)
            display(iframe)
            print('輸入驗證碼：')
            api_token = input()
            clear_output()
            print('登入成功!')
        except Exception as e:
            print('catch an error!')
            print(e)
            print('Go to this URL in a browser: https://ai.finlab.tw/api_token/')
            api_token = input('Enter your api_token:\n')
    role = 'free'
    if '#' in api_token:
        role = api_token[api_token.index('#') + 1:]
        api_token = api_token[:api_token.index('#')]
    os.environ['finlab_id_token'] = api_token
    os.environ['role'] = role

def get_token():

    if 'finlab_id_token' not in os.environ:
        login()

    return os.environ['finlab_id_token']
