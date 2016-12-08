

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.tag import Hannanum
from konlpy.utils import pprint
import re
from konlpy.tag import Kkma
from collections import Counter
import time

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
    s = input.split('\n')
    print("d : {}" , len(s))


def getContent(contents):
    for content in contents:
        p = content.get_text()
        # clearInput(p)
        if p == "":
            continue
        # print(p)
        pp = k.nouns(p)

        # print(pp)
        for i in range(len(pp)):
            # print(pp[i])
            temp = pp[i]
            if temp not in output:
                output[temp] = 0
            output[temp] += 1
            # count = Counter(pp)
            # for word, freq in count.most_common(10):
            #    print(word, freq)
    return output
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
output2 = {}

for p in text:
    #print(p)
    pp = k.nouns(p)

    #print(pp)
    #break
    for i in range(len(pp)):
        # print(pp[i])
        temp = pp[i]
        if temp not in output2:
            output2[temp] = 0
        output2[temp] += 1
        # count = Counter(pp)
        # for word, freq in count.most_common(10):
        #    print(word, freq)

count = Counter(output2)
for word, freq in count.most_common(100):
    print(word, freq)

checkTime = time.time() - startTime
print("time : ", checkTime)

#print(content)

#text = html2text(html)



#http://api.egloos.com/lennis/post/6072774.xml