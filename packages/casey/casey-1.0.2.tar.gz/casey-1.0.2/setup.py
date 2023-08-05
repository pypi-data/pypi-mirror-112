# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casey']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'casey',
    'version': '1.0.2',
    'description': 'A simple library to support various naming conventions and convert strings from one to another',
    'long_description': '# Casey\n\n[![PyPI](https://img.shields.io/pypi/v/casey)](https://pypi.org/project/casey/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/casey)](https://github.com/marverix/casey/actions/workflows/tests.yml)\n[![Codecov](https://img.shields.io/codecov/c/gh/marverix/casey?token=NPX0JP4458)](https://app.codecov.io/gh/marverix/casey)\n[![GitHub](https://img.shields.io/github/license/marverix/casey)](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0))\n[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmarverix%2Fcasey.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmarverix%2Fcasey?ref=badge_shield)\n\nA simple library to support various naming conventions and convert strings from one to another.\n\nCasey supports:\n\n* camelCase\n* PascalCase\n* kebab-case\n* snake_case and SNAKE_CASE\n\n## Usage\n\n### Installation\n\n```sh\npip install casey\n```\n\n### Sample\n\n```python\nimport casey\n\nsubject = "every 1 WORD is very IMPORTANT"\n\nsubject = casey.camel(subject)\nprint(subject)\n# Prints: every1WORDIsVeryIMPORTANT\n\nsubject = casey.kebab(subject)\nprint(subject)\n# Prints: every-1-WORD-is-very-IMPORTANT\n\nsubject = casey.pascal(subject)\nprint(subject)\n# Prints: Every1WORDIsVeryIMPORTANT\n\nsubject = casey.snake(subject)\nprint(subject)\n# Prints: every_1_WORD_is_very_IMPORTANT\n\nsubject = casey.snake(subject, upper=True)\nprint(subject)\n# Prints: EVERY_1_WORD_IS_VERY_IMPORTANT\n\n```\n\n### API\n\n* `clean(subject: str) -> str: ...`\n\n    Returns string with removed cases.\n\n* `camel(subject: str) -> str: ...`\n\n    Returns string in camelCase.\n  \n* `pascal(subject: str) -> str: ...`\n\n    Returns string in PascalCase.\n  \n* `kebab(subject: str) -> str: ...`\n\n    Returns string in kebab-case.\n  \n* `snake(subject: str) -> str: ...`\n\n    Returns string in snake_case.\n\n* `snake(subject: str, upper=False) -> str: ...`\n  \n    Returns string in snake_case.\n\n    If `upper` is `True`, it will convert whole subject to upper snake case.\n\n* `upper_first(subject: str) -> str: ...`\n  \n    Returns string with upper first letter (A-Z).\n  \n* `lower_first(subject: str) -> str: ...`\n\n    Returns string with lower first letter (A-Z).\n\n## License\n\nThis project is licensed under Apache-2.0 License - see the [LICENSE](LICENSE) file for details.\n\n\n[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmarverix%2Fcasey.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmarverix%2Fcasey?ref=badge_large)',
    'author': 'Marek Sierociński',
    'author_email': 'mareksierocinski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marverix/casey',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
