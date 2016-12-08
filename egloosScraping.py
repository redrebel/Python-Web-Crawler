import logging

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.tag import Hannanum
from konlpy.utils import pprint
import re
from konlpy.tag import Kkma
import time
from util import writer
import operator


logger = logging.getLogger()

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
    input = list(filter((lambda x: len(x) >= 2), input))
    return input

def scrap():
    """
    Kkma 는 nouns() 시 단어를 한번만 표시되고 속도가 느리지만 추출결과가 깔끔하다
    Hannanum 은 nouns() 시 단어를 매번 표시되고 (빈도수체크가능) 속도가 빠르지만 추출결과가 매끄럽지 않다.
    """
    global k
    k = Kkma()
    #k = Hannanum()
    k.nouns("intial ")

    global logger

    startTime = time.time()
    checkTime = time.time() - startTime
    logger.debug("intial time : %f", checkTime)
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

        pp = clearInput(pp)
        #print(pp)
        #break
        for i in range(len(pp)):
            # print(pp[i])
            temp = pp[i]
            if temp not in output:
                output[temp] = 0
            output[temp] += 1

    print("output :", output)
    count = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
    print("count :", count)
    for word, freq in count:
        print(word, freq)

    checkTime = time.time() - startTime
    print("time : ", checkTime)

    writer.saveCSV(count, "read/egloos.csv")
    #print(content)
    #http://api.egloos.com/lennis/post/6072774.xml