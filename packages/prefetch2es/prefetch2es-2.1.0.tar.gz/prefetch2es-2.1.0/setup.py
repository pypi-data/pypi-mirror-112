# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['prefetch2es']
install_requires = \
['elasticsearch>=7.8.0,<8.0.0',
 'libscca-python>=20200717,<20200718',
 'orjson>=3.4.6,<4.0.0',
 'tqdm>=4.48.0,<5.0.0',
 'urllib3>=1.26.5,<2.0.0']

entry_points = \
{'console_scripts': ['prefetch2es = prefetch2es:console_prefetch2es',
                     'prefetch2json = prefetch2es:console_prefetch2json']}

setup_kwargs = {
    'name': 'prefetch2es',
    'version': '2.1.0',
    'description': 'A library for fast import of Windows Prefetch into Elasticsearch.',
    'long_description': '# prefetch2es\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n[![PyPI version](https://badge.fury.io/py/prefetch2es.svg)](https://badge.fury.io/py/prefetch2es)\n[![Python Versions](https://img.shields.io/pypi/pyversions/prefetch2es.svg)](https://pypi.org/project/prefetch2es/)\n[![DockerHub Status](https://shields.io/docker/cloud/build/sumeshi/prefetch2es)](https://hub.docker.com/r/sumeshi/prefetch2es)\n\n![prefetch2es logo](https://gist.githubusercontent.com/sumeshi/c2f430d352ae763273faadf9616a29e5/raw/fd3921cb75a484af98d795f194e9e4cb16b88515/prefetch2es.svg)\n\nFast import of Windows Prefetch(.pf) into Elasticsearch.\n\nprefetch2es uses C library [libscca](https://github.com/libyal/libscca).\n\n## Usage\n\nWhen using from the commandline interface:\n\n```bash\n$ prefetch2es /path/to/your/file.pf\n```\n\nWhen using from the python-script:\n\n```python\nfrom prefetch2es.prefetch2es import prefetch2es\n\nif __name__ == \'__main__\':\n    filepath = \'/path/to/your/file.pf\'\n    prefetch2es(filepath)\n```\n\n## Arguments\nprefetch2es supports importing from multiple files.\n\n```\n$ prefetch2es file1.pf file2.pf file3.pf\n```\n\nAlso, possible to import recursively from a specific directory.\n\n```\n$ tree .\npffiles/\n  ├── file1.pf\n  ├── file2.pf\n  ├── file3.pf\n  └── subdirectory/\n    ├── file4.pf\n    └── subsubdirectory/\n      ├── file5.pf\n      └── file6.pf\n\n$ prefetch2es /pffiles/ # The Path is recursively expanded to file1~6.pf.\n```\n\n### Options\n```\n--host: \n    ElasticSearch host address\n    (default: localhost)\n\n--port: \n    ElasticSearch port number\n    (default: 9200)\n\n--index: \n    Index name\n    (default: prefetch2es)\n\n--scheme:\n  Scheme to use (http, or https)\n  (default: http)\n\n--pipeline\n  Elasticsearch Ingest Pipeline to use\n  (default: )\n\n--login:\n  The login to use if Elastic Security is enable\n  (default: )\n\n--pwd:\n  The password linked to the login provided\n  (default: )\n\n```\n\n## Examples\n\nWhen using from the commandline interface:\n\n```\n$ prefetch2es /path/to/your/file.pf --host=localhost --port=9200 --index=foobar\n```\n\nWhen using from the python-script:\n\n```python\nif __name__ == \'__main__\':\n    prefetch2es(\'/path/to/your/file.pf\', host=localhost, port=9200, index=\'foobar\')\n```\n\nWith the Amazon Elasticsearch Serivce (ES):\n\n```\n$ prefetch2es /path/to/your/file.pf --host=example.us-east-1.es.amazonaws.com --port=443 --scheme=https --index=foobar\n```\n\nWith credentials for Elastic Security:\n\n```\n$ prefetch2es /path/to/your/file.pf --host=localhost --port=9200 --index=foobar --login=elastic --pwd=******\n```\n\nNote: The current version does not verify the certificate.\n\n## Supported Prefetch versions\n\n- Windows XP\n- Windows 2003\n- Windows Vista (SP0)\n- Windows 7 (SP0)\n- Windows 8.1\n- Windows 10 1809\n- Windows 10 1903\n\nFor more information, please visit [libscca](https://github.com/libyal/libscca).\n\n## Appendix\n### prefetch2json\nExtra feature. 🍣 🍣 🍣\n\nConvert from Windows Prefetch to json file.\n\n```\n$ prefetch2json /path/to/your/file.pf /path/to/output/target.json\n```\n\nConvert from Windows Prefetch to Python dict object.\n\n```python\nfrom prefetch2es import prefetch2json\n\nif __name__ == \'__main__\':\n  filepath = \'/path/to/your/file.pf\'\n  result: dict = prefetch2json(filepath)\n```\n\n## Output Format Example\nUsing the sample prefetch file of [EricZimmerman/Prefetch](https://github.com/EricZimmerman/Prefetch) as an example.\n\n```\n{\n  "name": "CALC.EXE",\n  "filenames": [\n    "\\\\DEVICE\\\\HARDDISKVOLUME2\\\\WINDOWS\\\\SYSTEM32\\\\NTDLL.DLL",\n    ...\n  ],\n  "exec_count": 2,\n  "last_exec_time": 130974496211967500,\n  "format_version": 23,\n  "prefetch_hash": 2013131135,\n  "metrics": [\n    {\n      "filename": "\\\\DEVICE\\\\HARDDISKVOLUME2\\\\WINDOWS\\\\SYSTEM32\\\\NTDLL.DLL",\n      "file_reference": 281474976736310\n    },\n    ...\n  ],\n  "volumes": [\n    {\n      "path": "\\\\DEVICE\\\\HARDDISKVOLUME2",\n      "creation_time": 130974525181093750,\n      "serial_number": 2281737263\n    }\n  ]\n}\n```\n\n## Installation\n\n### via PyPI\n```\n$ pip install prefetch2es\n```\n\n### via DockerHub\n```\n$ docker pull sumeshi/prefetch2es:latest\n```\n\n## Run with Docker\nhttps://hub.docker.com/r/sumeshi/prefetch2es\n\n\n## prefetch2es\n```bash\n# "host.docker.internal" is only available in mac and windows environments.\n# For linux, use the --add-host option.\n$ docker run -t --rm -v $(pwd):/app sumeshi/prefetch2es:latest prefetch2es SAMPLE.pf --host=host.docker.internal\n```\n\n## prefetch2json\n```bash\n$ docker run -t --rm -v $(pwd):/app sumeshi/prefetch2es:latest prefetch2es SAMPLE.pf out.json\n```\n\nDo not use the "latest" image if at all possible.  \nThe "latest" image is not a released version, but is built from the contents of the master branch.\n\n## Contributing\n\n[CONTRIBUTING](https://github.com/sumeshi/prefetch2es/blob/master/CONTRIBUTING)\n\nThe source code for prefetch2es is hosted at GitHub, and you may download, fork, and review it from this repository(https://github.com/sumeshi/prefetch2es).\nPlease report issues and feature requests. :sushi: :sushi: :sushi:\n\n## License\nprefetch2es is released under the [MIT](https://github.com/sumeshi/prefetch2es/blob/master/LICENSE) License.\n\nPowered by [libscca](https://github.com/libyal/libscca).',
    'author': 'sumeshi',
    'author_email': 'j15322sn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumeshi/prefetch2es',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
