# JsonTestRunner
基于Unittest生成Json格式的测试结果,包含HTML/XML等,用于CICD以及其他需求

```python
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
    pass




# 例子
import unittest
import JsonTestRunner
start_dir = '/Users/yangyuexiong/Desktop/BasicService/BusinessModule'
discover = unittest.TestLoader().discover(start_dir=start_dir, pattern='test*.py')
# discover = unittest.defaultTestLoader.discover(start_dir='./BusinessModule', pattern='test*.py')
# discover.run(TestResult())

jtr = JsonTestRunner(tester='杨跃雄')
jtr.run(discover)
print(jtr.get_json_report())
# jsr.get_html_report()
# jsr.get_xml_report()
```