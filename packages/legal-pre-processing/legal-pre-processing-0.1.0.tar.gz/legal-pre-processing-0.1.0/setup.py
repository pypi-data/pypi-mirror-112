# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['legal_pre_processing']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF', 'nltk', 'poetry-version', 'unidecode']

setup_kwargs = {
    'name': 'legal-pre-processing',
    'version': '0.1.0',
    'description': 'Pre processing tools for documents with legal content.',
    'long_description': '# Legal Pre-processing\n\nPre processing tools for documents with legal content.\nAuthors: [Daniel Henrique Arruda Boeing](mailto:daniel.boeing@softplan.com.br) and [Israel Oliveira](mailto:israel.oliveira@softplan.com.br).\n\n[![Python 3.7](https://img.shields.io/badge/Python-3.7-gree.svg)](https://www.python.org/downloads/release/python-370/)\n[![Python 3.8](https://img.shields.io/badge/Python-3.8-gree.svg)](https://www.python.org/downloads/release/python-380/)\n[![Python 3.9](https://img.shields.io/badge/Python-3.9-gree.svg)](https://www.python.org/downloads/release/python-390/)\n\n## Usage:\n\n### Donwload the *JSON* files that could be used as examples.\n\n```bash\n$ mkdir -p data_dicts && cd data_dicts\n\n$ wget https://gitlab.com/israel.oliveira.softplan/legal-pre-processing/-/raw/master/data/LegalRegExPatterns.json\n\n$ wget https://gitlab.com/israel.oliveira.softplan/legal-pre-processing/-/raw/master/data/LegalStopwords.json\n\n$ wget https://gitlab.com/israel.oliveira.softplan/legal-pre-processing/-/raw/master/data/TesauroRevisado.json\n```\n\n### Load helper class and laod dictionaries.\n\n```python\n>>> from  legal_pre_processing.load_data import LoadDicts\n>>>\n>>> dicts = LoadDicts(\'legal_dicts/\')\n>>> dicts.List\n[\'LegalRegExPatterns\', \'TesauroRevisado\', \'LegalStopwords\']\n```\n\n### Load the class LegalPreprocess and and instantiate it.\n\n```python\n>>> from legal_pre_processing.legal_pre_processing import LegalPreprocess\n>>>\n>>> model = LegalPreprocess(domain_stopwords=dicts.LegalStopwords, tesauro=dicts.TesauroRevisado, regex_pattern=dicts.LegalRegExPatterns)\n```\n\n### Load a PDF file with [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) (or other extractor) and do some tests:\n\n```python\n>>> import fitz\n>>>\n>>> doc = fitz.open(\'some_pdf_file_with_legal_content.pdf\')\n>>> page = doc[page_number-1].get_text()\n>>> print(page)\n"...Com a concordância das partes foi utilizada prova emprestada em relação aos depoimentos de algumas testemunhas de defesa (decisões de 28/10/2016,  07/11/2016, de 10/11/2016 e de 09/02/2017, nos eventos 114, 175 e 199, e depoimentos nos eventos 187, 200, 287 e 513)...."\n>>> page_preprocess = model.ProcessText(page)\n>>> print(page_preprocess)\n"concordancia utilizada PROVA_EMPRESTADA relacao depoimentos algumas testemunhas defesa decisoes eventos depoimentos eventos"\n```\n',
    'author': 'Daniel Henrique Arruda Boeing',
    'author_email': 'daniel.boeing@softplan.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/israel.oliveira.softplan/legal-pre-processing.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
