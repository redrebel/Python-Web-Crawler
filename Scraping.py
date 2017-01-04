import logging
import os
import os.path
from urllib.request import urlopen
from bs4 import BeautifulSoup
import feedparser
import re
import time
from util import writer
from db import dao
import operator

from abc import ABCMeta, abstractmethod

logger = logging.getLogger()


class Scraping:
    __metaclass__ = ABCMeta # 추상클래스로 선언
    save_file_path = "read/"
    save_file_name = ""
    section_id = None
    section_id_padding = None

    def __init__(self):
        self.filter_words = None
        pass

    @abstractmethod  # 추상메소드 선언
    def scrap(self, text):
        pass

    @abstractmethod
    def proc(self, sid, feed_list):
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
        return time.strftime("%Y%m%d%H%M", time.localtime())

    def filter_word(self, word):
        if bool(re.search('\\d', word)) is True: return False
        if word in self.filter_words: return False
        return True

    def set_filter_words(self, file_path):
        _filter_words = []
        with open(file_path, 'r') as f:
            for line in f.readlines():
                if line[0] != '#': _filter_words.append(line.strip())

        self.filter_words = _filter_words
        print(self.filter_words)

    def get_feed_post_content(self, rss_url, stamp):
        self.save_file_name = self.section_id_padding + ".rss."+stamp
        logger.debug("get : %s", rss_url)

        # Parse the feed
        d = feedparser.parse(rss_url)
        self.scrap(d)

    def proc_feed_list(self, feed_list):
        i = -1;
        feedlist = []
        for line in feed_list:
            logger.debug('get : %s', line)
            i += 1
            stamp = self.get_date_time() + str(i).zfill(8)
            self.get_feed_post_content(line, stamp)

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
        # print("soup : ", soup)
        text_parts = soup.findAll(text=True)
        print(text_parts)

        self.scrap(text_parts)

    def get_rss_post_content_(self, rss_url, stamp):
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

    def proc_rss_list(self, feed_list):
        """
        source_list 목록을 받아서 처리한다
        :param feed_list:
        :return:
        """
        i = -1;
        for line in feed_list:
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
        # print('before text : ', text)
        # text = re.sub('\[[0-9]*\]', "", text)
        text = list(map(lambda x: self.clean_word(x), text))
        # print('after text : ', text)
        text = list(filter((lambda x: len(x) >= 2), text))
        return text

    def get_sorted_data(self,output):
        count = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
        print("count :", count)
        # for word, freq in count:
        #     print(word, freq)
        return count

    def save_txt(self, data):
        writer.save_txt(data, self.save_file_path + self.save_file_name + ".txt")

    def save_csv(self, data):
        writer.save_csv(data, self.save_file_path+self.save_file_name+".csv")

    def save_eng_db(self, data):
        dao.save_db(data, self.section_id, 'ENG')

    def save_kor_db(self, data):
        dao.save_db(data, self.section_id, 'KOR')

if __name__ == "__main__":

    url = "http://blog.cjred.net/rss/"
    # get_rss_post_content(url)
    # set_section_id(2)

    d = feedparser.parse('http://code.tutsplus.com/posts.atom')