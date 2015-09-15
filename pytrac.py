#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import config
import requests

token_match = re.compile(
    'name="__FORM_TOKEN" value="(?P<token>[^"]+)"', re.DOTALL)
version_match = re.compile(
    'name="version" value="(?P<version>\d+)"', re.DOTALL)

__version__ = '0.0.1'


class Trac(object):

    def __init__(self, trac_url, user, password, rememberme=1):
        self.base_url = trac_url
        self.login_url = '%s/login' % self.base_url
        self.user = user
        self.password = password
        self.rememberme = rememberme
        self.cookies = {}

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
        self.cookies = r.cookies
        self.cookies['trac_form_token'] = form_token
        return r.content

    def create(self, path, content='', comment=''):
        url = '%s/%s?action=edit' % (self.base_url, path)
        r = requests.get(url, cookies=self.cookies)
        response = r.content
        form_token = token_match.search(response).group('token')
        version = version_match.search(response).group('version') or 0
        form_token = self.cookies['trac_form_token']
        payload = {
            '__FORM_TOKEN': form_token,
            'from_editor': '1',
            'action': 'edit',
            'scroll_bar_pos': '36',
            'editrows': '8',
            '__EDITOR__1': 'textarea',
            'text': content,
            'version': version,
            'comment': comment,
            'save': '提交变更'
        }
        r = requests.post(url, data=payload, cookies=self.cookies)
        return r.content

if __name__ == '__main__':
    trac_url = config.TRAC_URL
    user = config.TRAC_USER
    password = config.TRAC_PASS
    t = Trac(trac_url, user, password)
    path = 'wiki/work/solos/2014/3/7'
    content = '''
{{{
#!rst

2014/3/7 日报
===============

pytrac
------

- add create function for pytrac.
- add config.py.sample file

}}}'''
    t.create(path, content)
