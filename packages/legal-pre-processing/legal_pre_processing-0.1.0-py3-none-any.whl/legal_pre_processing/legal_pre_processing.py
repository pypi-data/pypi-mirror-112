import re
import string
from typing import Dict
from typing import List
from typing import NewType

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from unidecode import unidecode


LegalStopwords = NewType("LegalStopwords", List[str])
Tesauro = NewType("Tesauro", Dict[str, str])
LegalRegExPatterns = NewType("LegalRegExPatterns", List[str])
LegalDocument = NewType("LegalDocument", str)
NormalizedLD = NewType("NormalizedLD", str)
LegalDocumentTokenized = NewType("LegalDocumentTokenized", str)
PalavrasPatternsType = NewType("PalavrasPatternsType", List[str])


class LegalPreprocess:
    """
    Classe de pré-processamento de textos jurídicos.

    O pré-processamento consiste em três etapas independentes entre si:
        a) Remoção de stopwords de domínio;
        b) Remoção de caracteres especiais, números e espaçamento duplo;
        c) Stemização de palavras;
        d) Aplicação de RegEx para detectar, dentre outros padrões, leis, artigos, códigos legais, precedentes, etc;
           os padrões detectados são transformados em tokens únicos, caso compostos por mais de um, e têm seus números
           convertidos em letras;
        e) Substituição de expressões constantes no Tesauro Jurídico pelos seus respectivos sinônimos, com vistas à padronização
           de termos de mesmo significado e grafias diferentes.
    """

    def __init__(
        self,
        domain_stopwords: LegalStopwords,
        tesauro: Tesauro,
        regex_pattern: LegalRegExPatterns,
        palavras_patterns: PalavrasPatternsType = None,
    ):
        self.domain_stopwords = set(domain_stopwords)
        self.tesauro = tesauro
        self.palavras_patterns = (
            set(palavras_patterns) if palavras_patterns is not None else set()
        )
        self.regex_pattern = "".join(regex_pattern)
        # self.txt = None

        # stemmer = nltk.stem.RSLPStemmer()
        self.stopwords = set(
            [
                w
                for w in set(
                    [
                        self.normalize_txt(w)
                        for w in domain_stopwords + stopwords.words("portuguese")
                    ]
                )
            ]
        )

        self.stemmer = nltk.stem.RSLPStemmer()
        self.detokenize = TreebankWordDetokenizer().detokenize
        self.tokenize = TreebankWordTokenizer().tokenize

        nz = self.normalize_txt

        tmp = [
            (nz(k), nz(v).replace(" ", "_").upper())
            for k, v in self.tesauro["equivalente"].items()
        ]
        tmp.extend(
            [
                (nz(w), nz(w).replace(" ", "_").upper())
                for w in self.tesauro["compostos"]
            ]
        )
        tmp = sorted(tmp, key=lambda x: len(x[0].split(" ")), reverse=True)  # 1
        self.descritor_dict = {k: w for (k, w) in tmp}
        self.descritor_str = "|".join([fr"\b{k}\b" for (k, _) in tmp])

        dict_numbers = {
            "1": "Q",
            "2": "W",
            "3": "E",
            "4": "R",
            "5": "T",
            "6": "Y",
            "7": "U",
            "8": "I",
            "9": "O",
            "0": "P",
        }
        self._dict = {" ": " "}
        self._dict.update({c: c for c in string.ascii_letters})
        self._dict.update(dict_numbers)

    def normalize_txt(self, txt: LegalDocument, upper=False) -> NormalizedLD:
        """
        texto final: minúsculas e remove acentuação, caracteres especiais e espaçamentos duplos
        """
        txt = re.sub(r"[^a-z0-9]", " ", unidecode(txt.lower()))
        txt = re.sub(r"\s{2,}", " ", txt)
        return txt.upper() if upper else txt

    # def joinWords(self, txt: NormalizedLD) -> NormalizedLD:
    #     """
    #     Arruma
    #     """
    #     tks = [w.lower() for w in txt.split() if len(w) >= 2]
    #     erros = []
    #     for i in range(len(tks) - 1):
    #         if tks[i] + tks[i + 1] in self.palavras_patterns:
    #             if tks[i] not in self.palavras_patterns:
    #                 erros.append((tks[i], tks[i + 1]))
    #             elif tks[i + 1] == "mente":
    #                 erros.append((tks[i], tks[i + 1]))
    #     # Revisar o `for` abaixo, pois é O(nm).
    #     for erro in erros:
    #         txt = txt.replace(erro[0] + " " + erro[1], erro[0] + erro[1])
    #     return txt

    def clean_number(self, txt: NormalizedLD) -> NormalizedLD:
        """
        Retira "_" entre números com objetivo de padronizar
        diferentes formas de escrita de dispositivos normativos
        """
        while re.search("_", txt) is not None:
            mt = re.search("(_)", txt)
            txt = txt[0 : mt.regs[1][0]] + txt[mt.regs[1][1] :]
        return txt

    def encode_number(self, txt: NormalizedLD) -> NormalizedLD:
        """
        Troca números por letras
        """
        return "".join(map(lambda c: self._dict[c], txt))

    def add_capture_groups(self, tupl):
        """
        Adiciona grupos de capturas encontrados por regex

        Notas:
            1: Evita que pontos no meio das leis, processos, etc., virem tokens diferentes
        """
        tmp = []
        for group in tupl:
            if group != "":
                tmp.append(group)
            joined_txt = self.clean_number("_".join(tmp))  # 1
            joined_txt = f" {joined_txt} "
        return joined_txt

    def find_law(
        self, txt: NormalizedLD, encode: bool = True, upper: bool = True
    ) -> NormalizedLD:
        """
        localiza padrões de entidades normativas e normaliza-os usando a função add_capture_groups


        Parâmetros:
            txt (NormalizedLD): Texto onde se espera encontrar expressões regulares.
            encode (bool): Opção para converter ou não números encontrados nas expressões regulares em letras. Padrão = True.
            upper (bool): Opção para deixar ou não o texto substituído todo em maiúsculas. Padrão = True.

        Returns:
            NormalizedLD: Texto com valores substituídos.

        Notas:
            1. Pressupõe o uso de normalize_txt.
            2. Remove os números do texto após realizar as substituições.
        """
        matches = re.findall(fr"{self.regex_pattern}", txt, flags=re.IGNORECASE)

        for m in matches:
            pattern = m[0]
            sub = self.add_capture_groups(m[1:])
            if encode:
                sub = self.encode_number(sub)
            if upper:
                sub = sub.upper()
            txt = re.sub(pattern, sub, txt)
        txt = re.sub("[0-9]", "", txt)
        txt = re.sub(r"\s{2,}", " ", txt)
        return txt

    def ss_token(
        self, txt: NormalizedLD, stopwords=False, stemmer=True
    ) -> NormalizedLD:
        """
        Stemização de tokens e remoção de Stopwords.

        Parâmetros:
            txt (NormalizedLD): Texto onde se espera encontrar expressões regulares.
            stop_words (bool): Opção para remover ou não stopwords. Padrão = False.
            stemmer (bool): Opção para deixar stemizar ou não o texto. Padrão = True.

        Returns:
            NormalizedLD: Texto com valores substituídos.

        Notas:
        1. Preserva de stemização tokens em maiúscula, pois presume que alguns
           trechos do texto já foram substituídos por outras funções e foram deixados em maiúscula.
        2. Stemiza as stopwords caso stemmer = True e stopwords = True
        3. Primeiro stemiza e depois remove stopwords.
        """
        txt = self.tokenize(txt)
        _stopwords = self.stopwords
        if stemmer:
            txt = [w if w.isupper() else self.stemmer.stem(w) for w in txt]
            if stopwords:
                _stopwords = set([self.stemmer.stem(w) for w in _stopwords])
        if stopwords:
            txt = [w for w in txt if w not in _stopwords]
        txt = self.detokenize(txt)
        return txt

    def ProcessText(
        self,
        txt: LegalDocument,
        stopwords: bool = True,
        stemmer: bool = False,
        # joinWords: bool = False,
        tesauro: bool = True,
        upper: bool = True,
    ) -> LegalDocumentTokenized:

        """Teste5 docstring"""
        txt = self.normalize_txt(str(txt))
        if self.regex_pattern:
            txt = self.find_law(txt, upper=upper)
        if tesauro:
            """
            Localiza chaves de um dicionario em um texto e as substitui
            pelos respectivos valores. Pressupoe uso da função normalize_txt.
            """
            txt = re.sub(
                self.descritor_str,
                lambda match: self.descritor_dict[
                    match.string[match.start() : match.end()]
                ],
                txt,
            )
        if stemmer or stopwords:
            txt = self.ss_token(txt, stopwords=stopwords, stemmer=stemmer)

        # if joinWords:
        #     txt = self.joinWords(txt)

        return txt


# EOF
