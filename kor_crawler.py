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


logger = logging.getLogger()


class KorCrawler:

    logger = logging.getLogger()
    save_file_path = "read/"
    save_file_name = ""
    # section_id = 0
    # section_id_padding = "0000"

    def __init__(self):
        pass
        self.set_knlpy()

    def proc(self, sid, feed_list):
        # Scraping.set_stamp(stamp)
        self.set_section_id(sid)
        startTime = time.time()
        self.proc_feed_list(feed_list)
        # self.get_rss_post_content("http://blog.cjred.net/rss/", "00")
        # self.get_egloos_post_content("lennis", "6072774")
        checkTime = time.time() - startTime
        logger.debug("work time : %f", checkTime)

    def get_date_time(self):
        return time.strftime("%Y%m%d%I%M", time.localtime())

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

    def set_section_id(self, sid):
        if not sid or sid is 0:
            logger.error("must have section_id!")
            exit()
        self.section_id = sid
        self.section_id_padding = str(self.section_id).zfill(8)

        self.save_file_path = self.save_file_path + self.section_id_padding + "/"
        print("save_file_path : ", self.save_file_path)
        if not os.path.exists(self.save_file_path):
            os.makedirs(self.save_file_path)

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

    def get_rss_post_content(self, rss_url, stamp):
        """
        rss 주소에서 글을 읽어와서 리턴한다.
        :param rss_url:
        :param stamp:
        :return:
        """
        self.save_file_name = self.section_id_padding + ".rss."+stamp
        logger.debug("get : %s", rss_url)
        response = urlopen(rss_url).read().decode("UTF-8")
        soup = BeautifulSoup(response, 'lxml')
        text_parts = soup.findAll(text=True)
        print(text_parts)

        self.scrap(text_parts)

    def proc_feed_list(self, feed_list):
        """
        feed 목록을 받아서 처리한다
        :param feed_list:
        :return:
        """
        date_time = time.strftime("%Y%m%d%I%M", time.localtime())
        i = -1;
        for line in feed_list:
            line = line.strip()
            print(line)
            i += 1
            stamp = date_time + str(i).zfill(8)

            self.get_rss_post_content(line, stamp)

    def html2text(self, html):
        soup = BeautifulSoup(html, "html.parser")
        text_parts = soup.findAll(text=True)
        # return '\n'.join(text_parts)
        return text_parts

    def xml2text(self, s):
        soup = BeautifulSoup(s, 'lxml')
        text_parts = soup.findAll(text=True)
        # text_parts = soup.findAll("content:encoded")
        # text_parts = soup.findAll("p")
        return text_parts

    def filter_word(self, word):
        word = re.sub('\\d', "", word)
        return word

    def clean_word(self, word):
        word = re.sub('\n', "", word)
        word = re.sub(' +', " ", word)
        word = re.sub(']]>', "", word)
        word = re.sub('http[^ ]*', "", word)
        return word

    def clearInput(self, text):
        # text = re.sub('\[[0-9]*\]', "", text)
        text = list(map(lambda x: self.clean_word(x), text))
        text = list(filter((lambda x: len(x) >= 2), text))
        return text

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

        print("output :", output)
        count = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
        print("count :", count)
        for word, freq in count:
            print(word, freq)

        checkTime = time.time() - startTime
        print("time : ", checkTime)

        writer.save_csv(count, self.save_file_path+self.save_file_name+".csv")
        # print(content)




if __name__ == "__main__":

    url = "http://blog.cjred.net/rss/"
    # get_rss_post_content(url)
    # set_section_id(2)