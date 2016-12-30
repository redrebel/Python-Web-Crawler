import logging
import os
import os.path
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.utils import pprint
import re
import time
from util import writer
import operator
from abc import ABCMeta, abstractmethod

logger = logging.getLogger()

class Scraping:
    __metaclass__ = ABCMeta # 추상클래스로 선언
    save_file_path = "read/"
    save_file_name = ""

    def __init__(self):
        pass

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

    def get_date_time(self):
        return time.strftime("%Y%m%d%I%M", time.localtime())

    @abstractmethod  # 추상메소드 선언
    def scrap(self, text_parts):
        pass

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
        i = -1;
        for line in feed_list:
            line = line.strip()
            print(line)
            i += 1
            stamp = self.get_date_time() + str(i).zfill(8)

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

    def get_sorted_data(self,output):
        count = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
        print("count :", count)
        for word, freq in count:
            print(word, freq)
        return count

    def save_csv(self, data):
        writer.save_csv(data, self.save_file_path+self.save_file_name+".csv")


if __name__ == "__main__":

    url = "http://blog.cjred.net/rss/"
    # get_rss_post_content(url)
    # set_section_id(2)