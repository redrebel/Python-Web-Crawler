import logging
import os, os.path
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
save_file_path = "read/"
save_file_name = ""
section_idx = 0
section_idx_padding = "0000"


def get_date_time():
    return time.strftime("%Y%m%d%I%M", time.localtime())


def set_knlpy(knlpy):
    if not knlpy :
        logger.error("must have knlpy!")
        exit()
    global k
    k = knlpy

def set_section_idx(sidx):
    if not sidx or sidx is 0:
        logger.error("must have section_idx!")
        exit()

    global section_idx
    section_idx = sidx
    global section_idx_padding
    section_idx_padding = str(section_idx).zfill(8)
    global save_file_path

    save_file_path = save_file_path + section_idx_padding + "/"
    if not os.path.exists(save_file_path):
        os.makedirs(save_file_path)

def get_egloos_post_content(id, post):
    date_time = get_date_time()
    stamp = date_time
    global save_file_name
    save_file_name = section_idx_padding + ".egloos."+stamp

    url = "http://api.egloos.com/" + id + "/post/" + post + ".json"
    print(url)
    response = urlopen(url).read().decode("UTF-8")
    responseJson = json.loads(response)
    #print(responseJson)
    html = responseJson.get("post").get("post_content")

    soup = BeautifulSoup(html, "html.parser")
    text = soup.findAll(text=True)
    scrap(text)


def get_rss_post_content(url, stamp):
    global save_file_name
    save_file_name = section_idx_padding + ".rss."+stamp

    response = urlopen(url).read().decode("UTF-8")
    soup = BeautifulSoup(response, 'lxml')
    text_parts = soup.findAll(text=True)

    #text = xml2text(response)
    print(text_parts)

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
    word = re.sub(']]>', "", word)
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
    text = clearInput(text)
    print(text)
    writer.save_txt(text, save_file_path+save_file_name+".txt")
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

    writer.save_csv(count, save_file_path+save_file_name+".csv")
    #print(content)


def proc_feed_list(feed_list):
    date_time = time.strftime("%Y%m%d%I%M", time.localtime())
    i = -1;
    for line in feed_list:
        print(line.strip())
        i += 1
        stamp = date_time + str(i).zfill(8)

        get_rss_post_content(line, stamp)


if __name__ == "__main__":

    url = "http://blog.cjred.net/rss/"
    #get_rss_post_content(url)
    set_section_idx(2)