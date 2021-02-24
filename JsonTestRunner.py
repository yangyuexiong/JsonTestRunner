# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 下午2:09
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : JsonTestRunner.py
# @Software: PyCharm

import io
import os
import sys
import json
import time
from xml.sax import saxutils
from datetime import datetime

import unittest
from unittest import TestResult


class TemplateMixin:
    """HTML模版"""

    HTML_TMPL = r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>%(title)s</title>
        <link
          rel="stylesheet"
          href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css"
        />
        <script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
        <script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
    
        <style>
          .panel-default > .panel-heading {
            background: none;
          }
          .panel-default > .panel-heading .btn {
            color: #fff;
          }
    
          .btn-group-wrapper .btn {
            width: 150px;
          }
          
          #backTop {
            position: fixed;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 16px;
            right: 30px;
            bottom: 30px;
            width: 40px;
            height: 40px;
            border-radius: 1000px;
            box-shadow: 0 0 10px 0 #ccc;
          }
          .btn-info,
          .btn-info:hover,
          .btn-info:focus,
          .btn-info:active {
            background-color: #337ab7;
            border-color: #337ab7;
          }

          .panel-body {
            white-space: pre-line;
          }
        </style>
      </head>
    <body>
    <div class="container-fluid">
    %(first_one)s
    %(first_two)s
    %(table)s
    </div>
    
    %(script)s
    </body>
    </html>
    """

    def __init__(self, test_result):
        if isinstance(test_result, dict):
            self.test_result = test_result
        else:
            raise TypeError('test_result 应该是一个 dict 类型')

    @classmethod
    def __generate_first_one(cls, **kwargs):
        """heading"""
        first_one = """<div class="heading">
        <h1 style="font-family: Microsoft YaHei">{title}</h1>
        <p class="attribute">
            <strong>
                测试人员:
            </strong>
            {tester}
        </p>
        <p class="attribute">
          <strong>
                开始时间:
          </strong> 
            {start_time}
        </p>
        <p class="attribute">
            <strong>
                合计耗时:
            </strong>
                {duration}
            </p>
        <p class="attribute">
          <strong>
                测试结果:
          </strong> 
          共:{all_count}
          通过:{success_count}
          失败:{failure_count}
          通过率:{pass_rate}
        </p>
        <p>
            {description}
        </p>
      </div>
        """.format(
            title=kwargs.get('title', 'title'),
            tester=kwargs.get('tester', 'tester'),
            start_time=kwargs.get('start_time', 'start_time'),
            duration=kwargs.get('duration', 'duration'),
            all_count=kwargs.get('all_count', 'all_count'),
            success_count=kwargs.get('success_count', 'success_count'),
            failure_count=kwargs.get('failure_count', 'failure_count'),
            pass_rate=kwargs.get('pass_rate', 'pass_rate'),
            description=kwargs.get('description', 'description'),
        )
        return first_one

    @classmethod
    def __generate_first_two(cls, **kwargs):
        """操作按钮"""
        first_two = """
        <div class="btn-group-wrapper">
            <button type="button" class="btn btn-primary">全部【{all_count}】</button>
            <button type="button" class="btn btn-success">成功【{success_count}】</button>
            <button type="button" class="btn btn-danger">失败【{failure_count}】</button>
        </div>
        """.format(
            all_count=kwargs.get('all_count', 'all_count'),
            success_count=kwargs.get('success_count', 'success_count'),
            failure_count=kwargs.get('failure_count', 'failure_count')
        )
        return first_two

    @classmethod
    def __generate_table(cls, **kwargs):
        """生成table"""
        rows = []
        result_list = kwargs.get('result_list')
        pass_rate = kwargs.get('pass_rate')
        for index, result in enumerate(result_list):
            result_code = result.get('result_code')
            tbody = """
            <tbody>
                <tr>
                    <td>
                    {case_class_doc}
                    {case_class}
                    </td>
                    <td>
                      <button class="btn btn-{status_btn} detail-btn">{status}</button>
                    </td>
                </tr>
            </tbody>
            <tbody class="detail hide {status_btn}">
              <tr>
                <td>
                    {case_method_doc}
                    {case_method_name}
                </td>
                <td>
                  <div class="panel panel-default">
                    <div class="panel-heading">
                      <h4 class="panel-title">
                        <a
                          class="btn btn-small btn-info"
                          data-toggle="collapse"
                          data-parent="#accordion"
                          href="#{href_case}"
                        >
                        详情
                        </a>
                      </h4>
                    </div>
                    <div id="{div_case}" class="panel-collapse collapse">
                      <div class="panel-body">
                        {output}
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
            """.format(
                case_class_doc=result.get('case_class_doc', 'case_class_doc'),
                case_class=result.get('case_class', 'case_class'),
                case_method_doc=result.get('case_class', 'case_class'),
                case_method_name=result.get('case_class', 'case_class'),
                status='正确' if result_code == 0 else '错误',
                status_btn='success' if result_code == 0 else 'danger',
                href_case=index,
                div_case=index,
                output=result.get('output', 'output')
            )
            rows.append(tbody)
        table_list = ''.join(rows)
        thead = """
        <thead>
          <tr>
            <th>用例集/测试用例</th>
            <th width="50%">详细</th>
          </tr>
        </thead>
        """

        tfoot = """
        <tfoot>
          <tr>
            <td>总计</td>
            <td>通过率:{pass_rate}</td>
          </tr>
        </tfoot>
        """.format(pass_rate=pass_rate)

        table_root = """
        <table class="table table-hover">
            {thead}
            {table_list}
            {tfoot}
        </table>
        """.format(
            thead=thead,
            table_list=table_list,
            tfoot=tfoot
        )
        return table_root

    @classmethod
    def __generate_script(cls):
        """script"""
        script = """
        <script>
          $(".detail-btn").on("click", function () {
            $(this).parents("tbody").next().toggleClass("hide");
          });
    
          $(".btn-group-wrapper .btn-primary").on("click", function () {
            $(".table tbody").removeClass("hide");
          });
    
          $(".btn-group-wrapper .btn-success").on("click", function () {
            $(".table .btn").parents("tbody").addClass("hide");
            $(".table .btn-success").parents("tbody").removeClass("hide");
          });
    
          $(".btn-group-wrapper .btn-danger").on("click", function () {
            $(".table .btn").parents("tbody").addClass("hide");
            $(".table .btn-danger").parents("tbody").removeClass("hide");
          });
    
          $("#backTop").on("click", () => {
            $("html,body").animate(
              {
                scrollTop: 0
              },
              200
            );
          });
        </script>
        """
        return script

    def generate_html_report(self):
        """生成html报告"""
        tr = self.test_result
        title = tr.get('title')
        description = tr.get('description')
        tester = tr.get('tester')
        start_time = tr.get('start_time')
        stop_time = tr.get('stop_time')
        duration = tr.get('duration')
        all_count = tr.get('all_count')
        success_count = tr.get('success_count')
        failure_count = tr.get('failure_count')
        error_count = tr.get('error_count')
        pass_rate = tr.get('pass_rate')
        result_list = tr.get('result_list')
        result_code = tr.get('result_code')

        first_one = self.__generate_first_one(**tr)
        first_two = self.__generate_first_two(**tr)
        table = self.__generate_table(**tr)
        script = self.__generate_script()
        html = self.HTML_TMPL % dict(
            title=saxutils.escape(title),
            first_one=first_one,
            first_two=first_two,
            table=table,
            script=script
        )
        return html


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

        self.module_dict = {}
        self.result_list = []

    def assemble_result_obj(self, test, result_code, output):
        """
        demo = {
            'module': {
                'cls': {
                    'def_list': [
                        {
                            'result_code': '',
                            'case_method_name': '',
                            'case_method_doc': '',
                            'output': ''
                        }
                    ]
                }
            }
        }
        """

        cls_module = test.__module__
        cls_name = test.__class__.__name__
        case_method_name = test._testMethodName
        case_method_doc = test._testMethodDoc
        case_dict = {
            'result_code': result_code,
            'case_method_name': case_method_name,
            'case_method_doc': case_method_doc,
            'output': '\n' + output
        }

        def __func():
            if self.module_dict.get(cls_module).get(cls_name):
                if self.module_dict.get(cls_module).get(cls_name).get('def_list'):
                    self.module_dict[cls_module][cls_name]['def_list'].append(case_dict)
                else:
                    self.module_dict[cls_module][cls_name]['def_list'] = []

            else:
                self.module_dict[cls_module][cls_name] = {}
                self.module_dict[cls_module][cls_name]['def_list'] = []
                self.module_dict[cls_module][cls_name]['def_list'].append(case_dict)

        if self.module_dict.get(cls_module):
            __func()
        else:
            self.module_dict[cls_module] = {
                'case_class': test.__module__,
                'case_class_doc': test.__doc__,
            }  # 创建module对象
            __func()

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

        self.assemble_result_obj(test, 0, output)
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

        self.assemble_result_obj(test, 1, output)
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

        self.assemble_result_obj(test, 2, output)
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
        运行Unittest的测试用例或测试套件
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
        # result_list = result.result_list
        result_list = result.module_dict
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

    def get_html_report(self, report_path=os.getcwd(), report_name=None):
        """生成 HTML 报告"""
        print(self.get_html_report.__doc__)
        if report_name:
            report_name = 'create_{}_'.format(time.strftime('%Y-%m-%d_%H:%M:%S')) + report_name
        else:
            report_name = 'Test_Report_{}_.html'.format(time.strftime('%Y-%m-%d_%H:%M:%S'))
        print('报告名称:{}'.format(report_name))

        report_path = report_path.split('BasicService')[0] + 'BasicService/reports'
        print('目录路径:{}'.format(report_path))

        final_path = '{}/{}'.format(report_path, report_name)
        print('绝对路径:{}'.format(final_path))

        self.test_result['title'] = self.title
        self.test_result['description'] = self.description
        self.test_result['tester'] = self.tester
        html_test_report = TemplateMixin(test_result=self.test_result)
        content = html_test_report.generate_html_report()

        with open(final_path, 'wb') as f:
            f.write(content.encode('utf8'))

    def get_xml_report(self, report_path=os.getcwd(), report_name=None):
        """生成 XML 报告"""
        print(self.get_xml_report.__doc__)
        # TODO 渲染 XML


if __name__ == '__main__':
    # 例子
    start_dir = '../JsonTestRunner/case'
    discover = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='test*.py')
    # discover.run(TestResult())

    jtr = JsonTestRunner(tester='杨跃雄')
    jtr.run(discover)
    print(jtr.get_json_report())
    print(json.dumps(jtr.get_json_report().get('result_list'), sort_keys=True, indent=4, separators=(', ', ': '),
                     ensure_ascii=False))
    jtr.get_html_report()
    # jtr.get_xml_report()
