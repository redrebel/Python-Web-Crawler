#!/usr/bin/evn python
# -*- coding: utf-8 -*-

#import requests
#from bs4 import BeautifulSoup

import feedparser   #파셔
#정규표현식
import re
from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.utils import pprint
from collections import Counter

d = feedparser.parse('http://blog.cjred.net/rss/5')
#print d['feed']
#print d['feed']['title']
#print d.entries
"""
    Kkma 는 nouns() 시 단어를 한번만 표시되고 속도가 느리지만 추출결과가 깔끔하다
    Hannanum 은 nouns() 시 단어를 매번 표시되고 (빈도수체크가능) 속도가 빠르지만 추출결과가 매끄럽지 않다.
"""
k = Kkma()
#k = Hannanum()
#p = k.nouns(u'학교를 학교 가니 학교 수업')
#print d['entries'][0]['content'][0]['value']
#print d['entries'][0]['summary']
# p = k.nouns(d['entries'][0]['content']['value'])
# pprint (p)
# count = Counter(p)

# for word, freq in count.most_common(5):
#     print word, freq

for e in d.entries:
    if 'summary' in e: summary=e.summary
    else: summary=e.description
    print e.title
    txt = re.compile(r'<[^>]+>').sub('', summary)
    txt = re.compile(r'https?[\S]+').sub('', txt)
    #txt = re.compile(r'htt+\S').sub('', txt)
        #print txt
    nouns = k.nouns(txt);
    #print nouns;
    #pprint (nouns)
    count = Counter(nouns)
    #count.most_common()
    for word, freq in count.most_common(10):
        print word, freq
