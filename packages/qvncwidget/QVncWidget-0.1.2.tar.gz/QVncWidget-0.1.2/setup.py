# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qvncwidget']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.4,<6.0.0',
 'Twisted>=21.2.0,<22.0.0',
 'pyDes>=2.0.1,<3.0.0',
 'service-identity>=21.1.0,<22.0.0']

setup_kwargs = {
    'name': 'qvncwidget',
    'version': '0.1.2',
    'description': 'Passive VNC QT Widget for Python using PyQt5',
    'long_description': '# pyQVNCWidget\nPassive VNC Widget for Python using PyQt5.\n\n_NOTE:_ This project is pretty much still in WiP status and I am struggling with the PIXEL_FORMAT.\\\nSo if someone knows a way to fix it or a better way of doing it in the first place, I would be happy about PRs ;)\n\n## How to install\n\n```bash\npip3 install qvncwidget\n```\n\n### TODO:\n- Proper error handling `onFatalError`\n- support for more than just RAW and RGB32 PIXEL_FORMATs\n- support for compression\n- (maybe) support for remote contol\n\n## Example (see /examples/example1.py)\n\n```python\nimport sys\nfrom PyQt5.QtWidgets import QApplication, QMainWindow\nfrom qvncwidget import QVNCWidget\n\nclass Window(QMainWindow):\n    def __init__(self):\n        super(Window, self).__init__()\n\n        self.initUI()\n\n    def initUI(self):\n        self.setWindowTitle("QVNCWidget")\n\n        self.vnc = QVNCWidget(\n            parent=self,\n            host="127.0.0.1", port=5900,\n            password="1234"\n        )\n        self.setCentralWidget(self.vnc)\n        self.vnc.start()\n\napp = QApplication(sys.argv)\nwindow = Window()\n#window.setFixedSize(800, 600)\nwindow.resize(800, 600)\nwindow.show()\n\nsys.exit(app.exec_())\n\n```\n',
    'author': 'zocker_160',
    'author_email': 'zocker1600@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zocker-160/pyQVNCWidget',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
