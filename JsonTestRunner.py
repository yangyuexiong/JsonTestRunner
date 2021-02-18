# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 下午2:09
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : JsonTestRunner.py
# @Software: PyCharm

import io
import os
import sys
import time
from datetime import datetime

import unittest
from unittest import TestResult


class TemplateMixin:
    """HTML模版"""

    def __init__(self, stream=sys.stdout):
        self.stream = stream


class OutputRedirector:
    """重定向标准输出或标准错误"""

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class TestResultExtension(TestResult):

    def __init__(self, verbosity=1):
        super().__init__()
        self.verbosity = verbosity
        self.this_stdout = None
        self.this_stderr = None
        self.output_buffer = None
        self.stdout_redirect = sys.stdout
        self.stderr_redirect = sys.stderr

        self.all_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.result_list = []

    def complete_output(self):
        """断开输出重定向和返回缓冲区,分别独立打印输出"""
        if self.this_stdout:
            sys.stdout = self.this_stdout
            sys.stderr = self.this_stderr
            self.this_stdout = None
            self.this_stderr = None
        return self.output_buffer.getvalue()

    def startTest(self, test):
        super().startTest(test)
        self.output_buffer = io.StringIO()  # 每次创建一个新的 StringIO 空间
        stdout_redirector.fp = self.output_buffer  # StringIO实例
        stderr_redirector.fp = self.output_buffer  # StringIO实例
        self.this_stdout = sys.stdout
        self.this_stderr = sys.stderr
        sys.stdout = stdout_redirector  # 将 StringIO 的值输出
        sys.stderr = stderr_redirector  # 将 StringIO 的值输出

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        super().addSuccess(test)
        output = self.complete_output()
        case_obj = {
            'result_code': 0,
            'test': test,
            'case_class': test.__module__,
            'case_class_doc': test.__doc__,
            'case_method_name': test._testMethodName,
            'case_method_doc': test._testMethodDoc,
            'output': '\n' + output
        }
        self.result_list.append(case_obj)
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        case_obj = {
            'result_code': 1,
            'test': test,
            'case_class': test.__module__,
            'case_class_doc': test.__doc__,
            'case_method_name': test._testMethodName,
            'case_method_doc': test._testMethodDoc,
            'output': output,
            'except_str': _exc_str
        }
        self.result_list.append(case_obj)
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        case_obj = {
            'result_code': 2,
            'test': test,
            'case_class': test.__module__,
            'case_class_doc': test.__doc__,
            'case_method_name': test._testMethodName,
            'case_method_doc': test._testMethodDoc,
            'output': output,
            'except_str': _exc_str
        }
        self.result_list.append(case_obj)
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')


class JsonTestRunner:
    """
    接收一个unittest测试套件,生成json格式的测试结果,包含HTML,XML的测试报告

    例子:
        # 测试套件集合
        discover = unittest.defaultTestLoader.discover('./test_path', pattern='test*.py')

        # JsonTestRunner实例化执行
        jtr = JsonTestRunner(result_format='json', title='自动化测试报告', description='xxx描述', tester='杨跃雄')
        jtr.run(discover)

    json:
        jtr.run(discover)
        jtr.get_json_report()

    html(查看文件目录即可):
        jtr.run(discover)
        jtr.get_html_report()

    xml(查看文件目录即可):
        jtr.run(discover)
        jtr.get_xml_report()

    """
    default_title = '测试报告'
    default_description = '描述...'
    default_tester = '测试人员'

    def __init__(self, title=None, description=None, tester=None):
        """
        :title: 报告标题(默认-default_title)
        :description: 报告描述内容(默认-default_description)
        :tester: 测试人员(默认-default_tester)
        """

        if not title:
            self.title = self.default_title
        else:
            self.title = title

        if not description:
            self.description = self.default_description
        else:
            self.description = description

        if not tester:
            self.tester = self.default_tester
        else:
            self.tester = tester

        self.start_time = datetime.now()
        self.stop_time = 0
        self.duration = 0
        self.test_result = {}

    def run(self, test):
        """
        :test: 测试套件
        运行Unittest的测试用例或测试套件。
        """
        # result = _TestResult(1)
        # result = TestResult()
        result = TestResultExtension(1)
        test(result)
        self.stop_time = datetime.now()
        self.generate_result(result)
        print('\nTime Elapsed: {}'.format(self.duration), file=sys.stderr)

    def generate_result(self, result):
        """输出 json 格式的测试结果(用于多方对接与扩展使用)"""
        self.stop_time = datetime.now()
        self.duration = str(self.stop_time - self.start_time)
        success_count = result.success_count
        failure_count = result.failure_count
        error_count = result.error_count
        all_count = success_count + failure_count + error_count
        result_list = result.result_list
        pass_rate = str("%.2f%%" % (float(success_count) / float(all_count) * 100))

        test_result = {
            "start_time": str(self.start_time)[:19],
            "stop_time": str(self.stop_time)[:19],
            "duration": self.duration,
            "all_count": all_count,
            "success_count": success_count,
            "failure_count": failure_count,
            "error_count": error_count,
            "pass_rate": pass_rate,
            "result_list": result_list
        }
        self.test_result = test_result

    def get_json_report(self):
        """获取 json 报告"""
        print(self.get_json_report.__doc__)
        return self.test_result

    def get_html_report(self, report_path=os.getcwd(),
                        report_name='Test_Report_{}_.html'.format(time.strftime('%Y-%m-%d_%H:%M:%S'))):
        """生成 HTML 报告"""
        print(self.get_html_report.__doc__)
        print(report_path)
        print(report_name)
        p = '{}/{}'.format(report_path, report_name)
        print(p)
        # TODO 渲染 HTML
        # with open(p, 'wb') as f:
        #     print('f:', f)
        # f.write()

    def get_xml_report(self, report_path=os.getcwd(),
                       report_name='Test_Report_{}_.xml'.format(time.strftime('%Y-%m-%d_%H:%M:%S'))):
        """生成 XML 报告"""
        print(self.get_xml_report.__doc__)
        print(report_path)
        print(report_name)
        p = '{}/{}'.format(report_path, report_name)
        print(p)
        # TODO 渲染 XML
        # with open(p, 'wb') as f:
        #     print('f:', f)
        # f.write()


if __name__ == '__main__':
    # 例子
    start_dir = '/Users/yangyuexiong/Desktop/BasicService/BusinessModule'
    discover = unittest.TestLoader().discover(start_dir=start_dir, pattern='test*.py')
    # discover = unittest.defaultTestLoader.discover(start_dir='./BusinessModule', pattern='test*.py')

    jtr = JsonTestRunner(tester='杨跃雄')
    jtr.run(discover)
    print(jtr.get_json_report())
    # jsr.get_html_report()
    # jsr.get_xml_report()
