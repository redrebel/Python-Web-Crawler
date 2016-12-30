import logging
import os
import os.path
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.utils import pprint
import re
import time
from util import writer
import operator
from Scraping import Scraping

logger = logging.getLogger()

class KorCrawler(Scraping):

    def __init__(self):
        self.set_knlpy()

    def proc(self, sid, feed_list):
        self.set_section_id(sid)
        startTime = time.time()
        self.proc_feed_list(feed_list)
        # self.get_rss_post_content("http://blog.cjred.net/rss/", "00")
        # self.get_egloos_post_content("lennis", "6072774")
        checkTime = time.time() - startTime
        logger.debug("work time : %f", checkTime)

    def set_knlpy(self):
        """
        Kkma 는 nouns() 시 단어를 한번만 표시되고 속도가 느리지만 추출결과가 깔끔하다
        Hannanum 은 nouns() 시 단어를 매번 표시되고 (빈도수체크가능) 속도가 빠르지만 추출결과가 매끄럽지 않다.
        """
        k = Kkma()
        # k = Hannanum()
        if not k:
            logger.error("must have knlpy!")
            exit()

        startTime = time.time()
        k.nouns("intial ")
        self.k = k
        checkTime = time.time() - startTime
        logger.debug("intial time : %f", checkTime)


    def get_egloos_post_content(self, id, post):
        date_time = self.get_date_time()
        stamp = date_time
        self.save_file_name = self.section_id_padding + ".egloos."+stamp

        api_url = "http://api.egloos.com/" + id + "/post/" + post + ".json"
        logger.debug("get : ", api_url)
        response = urlopen(api_url).read().decode("UTF-8")
        responseJson = json.loads(response)
        # print(responseJson)
        html = responseJson.get("post").get("post_content")

        soup = BeautifulSoup(html, "html.parser")
        text = soup.findAll(text=True)
        self.scrap(text)

    def filter_word(self, word):
        word = re.sub('\\d', "", word)
        return word

    def scrap(self, text):
        startTime = time.time()
        text = self.clearInput(text)
        print(text)
        writer.save_txt(text, self.save_file_path+self.save_file_name+".txt")
        output = {}

        for p in text:
            # print(p)
            p = self.clean_word(p)
            if len(p) < 2:
                continue

            pp = self.k.nouns(p)

            pp = self.clearInput(pp)
            # print(pp)
            # break
            if len(pp) == 0:
                continue
            for i in range(len(pp)):
                # print(pp[i])
                temp = pp[i]
                if temp not in output:
                    output[temp] = 0
                output[temp] += 1

        checkTime = time.time() - startTime
        print("time : ", checkTime)

        print("output :", output)
        data = self.get_sorted_data(output)
        self.save_csv(data)

        # print(content)


if __name__ == "__main__":

    url = "http://blog.cjred.net/rss/"
    # get_rss_post_content(url)
    # set_section_id(2)