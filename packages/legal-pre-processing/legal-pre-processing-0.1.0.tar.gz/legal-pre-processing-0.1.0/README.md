# Legal Pre-processing

Pre processing tools for documents with legal content.
Authors: [Daniel Henrique Arruda Boeing](mailto:daniel.boeing@softplan.com.br) and [Israel Oliveira](mailto:israel.oliveira@softplan.com.br).

[![Python 3.7](https://img.shields.io/badge/Python-3.7-gree.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/Python-3.8-gree.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-gree.svg)](https://www.python.org/downloads/release/python-390/)

## Usage:

### Donwload the *JSON* files that could be used as examples.

```bash
$ mkdir -p data_dicts && cd data_dicts

$ wget https://gitlab.com/israel.oliveira.softplan/legal-pre-processing/-/raw/master/data/LegalRegExPatterns.json

$ wget https://gitlab.com/israel.oliveira.softplan/legal-pre-processing/-/raw/master/data/LegalStopwords.json

$ wget https://gitlab.com/israel.oliveira.softplan/legal-pre-processing/-/raw/master/data/TesauroRevisado.json
```

### Load helper class and laod dictionaries.

```python
>>> from  legal_pre_processing.load_data import LoadDicts
>>>
>>> dicts = LoadDicts('legal_dicts/')
>>> dicts.List
['LegalRegExPatterns', 'TesauroRevisado', 'LegalStopwords']
```

### Load the class LegalPreprocess and and instantiate it.

```python
>>> from legal_pre_processing.legal_pre_processing import LegalPreprocess
>>>
>>> model = LegalPreprocess(domain_stopwords=dicts.LegalStopwords, tesauro=dicts.TesauroRevisado, regex_pattern=dicts.LegalRegExPatterns)
```

### Load a PDF file with [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) (or other extractor) and do some tests:

```python
>>> import fitz
>>>
>>> doc = fitz.open('some_pdf_file_with_legal_content.pdf')
>>> page = doc[page_number-1].get_text()
>>> print(page)
"...Com a concordância das partes foi utilizada prova emprestada em relação aos depoimentos de algumas testemunhas de defesa (decisões de 28/10/2016,  07/11/2016, de 10/11/2016 e de 09/02/2017, nos eventos 114, 175 e 199, e depoimentos nos eventos 187, 200, 287 e 513)...."
>>> page_preprocess = model.ProcessText(page)
>>> print(page_preprocess)
"concordancia utilizada PROVA_EMPRESTADA relacao depoimentos algumas testemunhas defesa decisoes eventos depoimentos eventos"
```
