# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s_tool']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141.0,<4.0.0', 'webdriver-manager>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 's-tool',
    'version': '0.0.2',
    'description': 'Selenium wrapper to make your life easy.',
    'long_description': '# S-Tool\n\n![S-tool](https://user-images.githubusercontent.com/33047641/125023819-41998700-e09d-11eb-8076-7fad81f98f70.png)\n\n## Selenium wrapper to make your life easy\n\n![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python)\n![selemium](https://img.shields.io/badge/Selenium-e5dfde?style=for-the-badge&logo=selenium)\n![s-tool](https://img.shields.io/badge/S-Tool-3776AB?style=for-the-badge)\n![Python-World](https://img.shields.io/badge/Python-World-FFD43B?style=for-the-badge&logo=python&logoColor=white)\n\n## Table of Contents\n\n- [Key Features](#key-features)\n- [How To Use](#how-to-use)\n- [Examples](#examples)\n- [Todo](#todo)\n- [License](#license)\n\n## Key Features\n\n- WebDriver\n  - Manage multiple web drivers such as chrome,chromium,firefox.\n- Different Utilities\n  - Retrieve element with 5 different attribute.\n  - Perform clicks on element\n  - Take full page and element screenshot.\n  - Hide and show elements.\n  - Information filling on different form elements such as text,radio,checkbox.\n  - Retrieves current cookies from browser.\n  - Retrieve url and web page source\n- Element Parser\n  - table Information\n  - Retrieve dropdown options in dictionary\n\n## How To Use\n\n### Install using PYPI\n\n```bash\npip install s-tool\n```\n\n### Setup for development\n\nTo clone and run this application, you\'ll need [Git](https://git-scm.com) and\n[Poetry](https://python-poetry.org/) and [python Version ^3.8](http://python.org/)\n\n```bash\n# Clone this repository\ngit clone https://github.com/Python-World/s-tool.git\n\n# Go into the repository\ncd s-tool\n\n# Install dependencies\npoetry config virtualenvs.in-project true\npoetry install\n\n# Start Poetry shell\npoetry shell\n```\n\nNote: If you\'re doing development setup, [see this guide](CONTRIBUTING)\n\n## Examples\n\n### Example 1\n\n```python\n"""Example code with class"""\n\nfrom s_tool.driver import SeleniumDriver\n\n\nclass SBot(SeleniumDriver):\n    """Example Bot using s-tool"""\n\n    def __init__(self, *args, **kwargs):\n        super().__init__(*args, **kwargs)\n\n    def run(self):\n        self.get("https://google.com")\n        sessionid = self.session()\n        url = self.url()\n        cookies = self.cookies()\n\n        # print sessionid,url,cookies\n        print(f"\\nurl     :   {url} \\nsession :   {sessionid}\\ncookies :   {cookies}\\n")\n\n\nbot = SBot("firefox", headless=True)  # change headless=False to run with gui mode\nbot.run()\nbot.close()\n\n```\n\n### Example 2\n\n```python\n"""Example code with context manager"""\n\nfrom s_tool.driver import SeleniumDriver as SBot\n\nwith SBot("firefox", headless=True) as obj:\n    obj.get("https://google.com")\n    sessionid = obj.session()\n    url = obj.url()\n    cookies = obj.cookies()\n\n    # print sessionid,url,cookies\n    print(f"\\nurl     :   {url} \\nsession :   {sessionid}\\ncookies :   {cookies}\\n")\n\n```\n\n## Todo\n\n- Web driver utilities\n  - Scrolling element and page.\n  - Handling popup and alert boxes.\n  - Switching windows,frame,tabs,iframes.\n  - logger.\n- Element Parser\n  - list\n  - radio and checkboxes\n\nNote: If you have any idea to improve or optimized in better way\n[create issue](https://github.com/Python-World/s-tool/issues/new) for discussion.\n\n## License\n\n[MIT](LICENSE)\n',
    'author': 'Ravishankar Chavare',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Python-World/s-tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
