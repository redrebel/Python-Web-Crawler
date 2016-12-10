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
import lxml
import string

logger = logging.getLogger()
save_file_name = ""


def set_knlpy(knlpy):
    global k
    k = knlpy


def get_egloos_post_content(id, post):

    global save_file_name
    save_file_name = "egloos"

    url = "http://api.egloos.com/" + id + "/post/" + post + ".json"
    print(url)
    response = urlopen(url).read().decode("UTF-8")
    responseJson = json.loads(response)
    #print(responseJson)
    html = responseJson.get("post").get("post_content")

    soup = BeautifulSoup(html, "html.parser")
    text = soup.findAll(text=True)
    scrap(text)


def get_rss_post_content(knlpy, url, max_page=100):
    global save_file_name
    save_file_name = "rss"
    response = urlopen(url).read().decode("UTF-8")
    soup = BeautifulSoup(response, 'lxml')
    text_parts = soup.findAll(text=True)

    #text = xml2text(response)
    print(text_parts)
    t = clearInput(text_parts)
    print(t)
    scrap(text_parts)


def html2text(html):
    soup = BeautifulSoup(html, "html.parser")
    text_parts = soup.findAll(text=True)
    #return '\n'.join(text_parts)
    return text_parts


def xml2text(s):
    soup = BeautifulSoup(s, 'lxml')
    text_parts = soup.findAll(text=True)
    #text_parts = soup.findAll("content:encoded")
    #text_parts = soup.findAll("p")
    return text_parts


def filter_word(word):
    word = re.sub('\\d', "", word)
    return word


def clean_word(word):
    word = re.sub('\n', "", word)
    word = re.sub(' +', " ", word)
    word = re.sub('http[^ ]*', "", word)
    return word


def clearInput(text):
    #text = re.sub('\[[0-9]*\]', "", text)
    text = list(map(lambda x: clean_word(x), text))
    text = list(filter((lambda x: len(x) >= 2), text))
    return text




def scrap(text):

    startTime = time.time()
    checkTime = time.time() - startTime
    print("network time : ", checkTime)
    startTime = time.time()

    print(text)
    writer.saveTxt(text, "read/"+save_file_name+".txt")
    output = {}

    for p in text:
        #print(p)
        p = clean_word(p)
        if len(p) < 2:
            continue

        pp = k.nouns(p)

        pp = clearInput(pp)
        #print(pp)
        #break
        if len(pp) == 0:
            continue
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

    writer.saveCSV(count, "read/"+save_file_name+".csv")
    #print(content)


if __name__ == "__main__":

    url = "http://blog.cjred.net/rss/"
    get_rss_post_content(url)