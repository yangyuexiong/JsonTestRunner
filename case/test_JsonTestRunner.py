# -*- coding: utf-8 -*-
# @Time    : 2021/2/19 下午3:55
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_JsonTestRunner.py
# @Software: PyCharm

import unittest


class TestJsonTestRunner(unittest.TestCase):
    """测试 JsonTestRunner"""

    def test_001(self):
        """正确输出001"""
        print('正确输出')

    def test_002(self):
        """错误输出002"""
        print('错误输出')
