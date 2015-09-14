
# -*- coding:utf-8 -*-

import sys

def mock_config():
    global TRAC_USER
    global TRAC_PASS
    global TRAC_URL
    TRAC_USER = 'user'
    TRAC_PASS = 'pass'
    TRAC_URL = 'url'

sys.modules['config'] = mock_config

sys.path.append('../src/')

from pytrac import Trac
import unittest
from mock import Mock, call, patch


class DefaultTestCase(unittest.TestCase):
    def setUp(self):
        self.pytrac = Trac('http://trac_url',
                           'http://trac_url/login',
                           'user', 'password')
        self.post_patcher = patch("requests.post")
        self.mock_post = self.post_patcher.start()
        self.get_patcher = patch("requests.get")
        self.mock_get = self.get_patcher.start()
        self.token_match_patcher = patch("pytrac.token_match")
        self.mock_group = self.token_match_patcher.start()

        # Setting values of default mocks
        
        self.mock_group.search.return_value.group.return_value = 'hulahoop'
        self.mock_post.return_value.content = 'hulahoop'
        self.mock_get.return_value.content = 'token'
        self.mock_get.return_value.cookies = 'cookies'

    def tearDown(self):
        self.post_patcher.stop()
        self.get_patcher.stop()
        self.token_match_patcher.stop()

    def test_login(self):
        login_result = self.pytrac.login()
        self.assertEqual(login_result, 'hulahoop')
        self.assertListEqual(self.mock_post.call_args_list,
                             [call('http://trac_url/login',
                                   cookies='cookies',
                                   data={'rememberme': 'password',
                                         '__FORM_TOKEN': 'hulahoop',
                                         'password': 'user',
                                         'user': 'http://trac_url/login'})])

    @patch("pytrac.version_match")
    def test_create(self, mock_group2):
        mock_group2.search.return_value.group.return_value = 'hulahoop'
        self.pytrac.cookies['trac_form_token'] = 'cookie'
        create_result = self.pytrac.create('path', 'content', 'comment')
        self.assertEqual(create_result, 'hulahoop')
        self.assertListEqual(self.mock_post.call_args_list,
                             [call('http://trac_url/path?action=edit',
                                   cookies={'trac_form_token': 'cookie'},
                                   data={'comment': 'comment',
                                         'save': '\xe6\x8f\x90\xe4\xba\xa4\xe5\x8f\x98\xe6\x9b\xb4',
                                         '__FORM_TOKEN': 'cookie', 'editrows': '8',
                                         'version': 'hulahoop', 'action': 'edit',
                                         'text': 'content', 'from_editor': '1',
                                         'scroll_bar_pos': '36',
                                         '__EDITOR__1': 'textarea'})])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DefaultTestCase('test_version'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=3)
