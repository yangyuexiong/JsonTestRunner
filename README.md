# JsonTestRunner
基于Unittest生成Json格式的测试结果,包含HTML/XML等测试报告,用于CICD以及其他需求

ps:感谢 HTMLTestRunner 作者的实现思路

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

    报告生成:
        jtr.generate_report('html')
        jtr.generate_report('xml')
        jtr.generate_report('excel')

    """
    pass




# 例子
import unittest
import JsonTestRunner

start_dir = '../JsonTestRunner/case'
discover = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='test*.py')

jtr = JsonTestRunner(tester='杨跃雄')
jtr.run(discover)

print(jtr.get_json_report())
jtr.generate_report('html')
# jtr.generate_report('xml')
# jtr.generate_report('excel')
```