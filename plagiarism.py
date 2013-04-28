#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from io import StringIO, BytesIO
import sys, re, string, logging
from collections import defaultdict
from datetime import datetime

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter

from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import SnowballStemmer
import nltk.data

from network import download
from ssk import SSK

def timestr():
    return datetime.now().strftime('%H:%M:%S')

def decodepdf(fp, debug = False):
    with StringIO() as outfp:
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, outfp)
        logging.disable(logging.WARNING)
        if debug: print("processing pdf begin ({0})".format(timestr()))
        process_pdf(rsrcmgr, device, fp)
        if debug: print("processing pdf ended ({0})".format(timestr()))
        logging.disable(logging.NOTSET)
        return outfp.getvalue()

def decodetxt(fp):
    return fp.read()

def readfile(file, debug = False):
    try:
        if file.endswith('.txt'):
            with open(file, 'r') as fp:
                return fp.read()
        elif file.endswith('.pdf'):
            with open(file, 'rb') as fp:
                return decodepdf(fp, debug=debug)
    except KeyboardInterrupt:
        raise
    except:
        pass

def downloadfile(url, debug = False):
    data = download(url)
    try:
        if url.endswith('.txt'):
            return data.decode('utf-8')
        elif url.endswith('.pdf'):
            return decodepdf(BytesIO(data), debug=debug)
    except KeyboardInterrupt:
        raise
    except:
        pass

words_cache = {}

def getwords(text, langs=["english", "russian"], debug = False):
    key = (text, tuple(langs))
    if (key in words_cache):
        if debug: print("found words in cache")
        return words_cache[key]
    punct = re.compile('[%s0-9\–]' % re.escape(string.punctuation))
    
    if debug: print("tokenize begin ({0})".format(timestr()))
    words = TreebankWordTokenizer().tokenize(str(text));
    if debug: print("tokenize ended ({0})".format(timestr()))

    if debug: print("del short words begin ({0})".format(timestr()))
    words[:] = [word for word in words if len(word)>2]
    if debug: print("del short words ended ({0})".format(timestr()))

    if debug: print("punctuation begin ({0})".format(timestr()))
    words[:] = [word for word in words if punct.sub("", word) == word]
    if debug: print("punctuation ended ({0})".format(timestr()))

    if debug: print("stopwords begin ({0})".format(timestr()))
    words[:] = [word.lower() for word in words]
    stops = [stopwords.words(lang) for lang in langs]
    for stop in stops:
        words[:] = [word for word in words if word not in stop]
    if debug: print("stopwords ended ({0})".format(timestr()))

    if debug: print("stemming begin ({0})".format(timestr()))
    stemmers = [SnowballStemmer(lang) for lang in langs]
    for stemmer in stemmers:
        words[:] = [stemmer.stem(word) for word in words]
    if debug: print("stemming ended ({0})".format(timestr()))

    words_cache[key] = words
    return words

def getkeywords(text, langs=["english", "russian"], num = 10, debug = False):
    
    words = getwords(text, langs, debug=debug)
    
    wordsCount = defaultdict(int)
    for word in words:
        wordsCount[word] += 1
    
    if debug: print("sorting begin ({0})".format(timestr()))
    words = sorted(wordsCount.items(), key=lambda x: x[1], reverse=True)[:num]
    if debug: print("sorting ended ({0})".format(timestr()))
    
    words[:] = [word for (word, cnt) in words]
    
    return words

def evaluate(text1, text2, langs = ["english", "russian"], debug = False):
    text1 = getwords(text1, langs=langs, debug=debug)
    text2 = getwords(text2, langs=langs, debug=debug)

    block_sz = 100
    threshold = 0.1
    text1s = [text1[i:i+block_sz] for i in range(0, len(text1), block_sz)]
    text2s = [text2[i:i+block_sz] for i in range(0, len(text2), block_sz)]
    
    blocks = []
    for s in text1s:
        for t in text2s:
            res = SSK(s, t).solve(3)
            if res > threshold:
                blocks.append((res, s, t))
    
    return blocks