

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.tag import Hannanum
from konlpy.utils import pprint
import re
from konlpy.tag import Kkma
from collections import Counter
import time
from util import writer
import operator

def getPostContent(id, post):
    url = "http://api.egloos.com/" + id + "/post/" + post + ".json"
    print(url)
    response = urlopen(url).read().decode("UTF-8")
    responseJson = json.loads(response)
    #print(responseJson)
    return responseJson.get("post").get("post_content")

def html2text(html):
    soup = BeautifulSoup(html, "html.parser")
    text_parts = soup.findAll(text=True)
    return '\n'.join(text_parts)


def clearInput(input):
    input = filter((lambda x: len(x) >= 2), input)
    return input



startTime = time.time()

"""
    Kkma 는 nouns() 시 단어를 한번만 표시되고 속도가 느리지만 추출결과가 깔끔하다
    Hannanum 은 nouns() 시 단어를 매번 표시되고 (빈도수체크가능) 속도가 빠르지만 추출결과가 매끄럽지 않다.
"""
k = Kkma()
#k = Hannanum()
pp = k.nouns("intial ")
checkTime = time.time() - startTime
print("intial time : ", checkTime)
startTime = time.time()

html = getPostContent("lennis","6072774")
#print(html)
checkTime = time.time() - startTime
print("network time : ", checkTime)
startTime = time.time()

soup = BeautifulSoup(html, "html.parser")
text = soup.findAll(text=True)
print(text)
#writer.saveTxt(text, "read/egloos.txt")
output = {}

for p in text:
    #print(p)
    pp = k.nouns(p)

    #print(pp)
    #break
    for i in range(len(pp)):
        # print(pp[i])
        temp = pp[i]
        if len(temp) < 2:
            continue
        if temp not in output:
            output[temp] = 0
        output[temp] += 1
        # count = Counter(pp)
        # for word, freq in count.most_common(10):
        #    print(word, freq)

count = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
#output = clearInput(output)
#count = Counter(output)
for word, freq in count:
    print(word, freq)

checkTime = time.time() - startTime
print("time : ", checkTime)

writer.saveCSV(count, "read/egloos.csv")
#print(content)

#text = html2text(html)



#http://api.egloos.com/lennis/post/6072774.xml