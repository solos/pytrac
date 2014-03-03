#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

token_match = re.compile(
    'name="__FORM_TOKEN" value="(?P<token>[^"]+)"', re.DOTALL)


class Trac(object):

    def __init__(self, trac_url, user, password, rememberme=1):
        self.base_url = trac_url
        self.login_url = '%s/login' % self.base_url
        self.user = user
        self.password = password
        self.rememberme = rememberme

    def login(self):
        r = requests.get(self.login_url)
        content = r.content
        cookies = r.cookies
        form_token = token_match.search(content).group('token')
        payload = {
            'user': self.user,
            'password': self.password,
            'rememberme': self.rememberme,
            '__FORM_TOKEN': form_token
        }
        r = requests.post(self.login_url, data=payload, cookies=cookies)
        return r.cookies

if __name__ == '__main__':
    trac_url = ''
    user = ''
    password = ''
    t = Trac(trac_url, user, password)
    print t.login()
