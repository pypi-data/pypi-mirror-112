# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commando']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycommando',
    'version': '1.1.0',
    'description': 'A framework for batch processing.',
    'long_description': '# Commando\n\nCommando is a framework for batch processing.\n\nVersioning of this repository follows [Semantic Versioning 2.0.0](https://semver.org/)\n\n`subprocess.run` をラッピングしているので外部コマンドのために面倒な記述をしなくて良いのが特徴。\n\nコマンドラインツールを脳筋で実行していくバッチ処理のためのフレームワーク。\n基本的にPythonの構文でワークフローを構築できるので、バッチ処理での変数の取り回しなどがしやすいのがメリット。\n\nShell Script や Bat ファイルを書かなくても実行したいコマンドさえわかっていればバッチ処理が書ける。\n\n## Concept\n- バッチ処理ワークフローを構築するためのフレームワーク\n- 逐次処理で書く\n- 外部コマンドに関しては subprocess.run()が走る\n\n\n## Feature\n- `add()`\n    - add command\n- `execute(): `\n    - Execute the added command.\n- Process them in the order they were added.\n- Functions can also be executed as commands\n\n## Usage\n\ninstall\n```shell\npip install pycommando\n```\n\nscript\n```python\nimport logging\n\nfrom commando import commando\n\nlogging.basicConfig(filename="test.log", level=logging.DEBUG)\n\n\ndef zero():\n    1 / 0\n\n\ncommando.add("mkdir test")\ncommando.add("touch test\\\\test.txt")\ncommando.add(zero)\n\ncommando.execute()\n```\n\nlog\n```log\nDEBUG:commando.commando:mkdir test\nDEBUG:commando.commando:touch test\\test.txt\nDEBUG:commando.commando:<function zero at 0x01A177C0>\nERROR:commando.commando:Could not execute function\nTraceback (most recent call last):\n  File "C:\\venv\\lib\\site-packages\\commando\\commando.py", line 28, in execute\n    cmd()\n  File "main.py", line 10, in zero\n    1 / 0\nZeroDivisionError: division by zero\n```\n',
    'author': 'zztkm',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
