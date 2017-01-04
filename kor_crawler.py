import logging
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.utils import pprint
import re
import time
from Scraping import Scraping

logger = logging.getLogger()


class KorCrawler(Scraping):

    def __init__(self):
        self.set_knlpy()
        self.set_filter_words('source_list/KOR/KOR_filterwords.txt')
        pass

    def proc(self, section_id, source_type, source_list):
        self.set_section_id(section_id)
        startTime = time.time()
        if source_type == 'RSS':
            self.proc_list(source_list, type=self.get_rss_post_content)
        elif source_type == 'EGLOOS':
            self.get_egloos_post_content("lennis", "6072774")
        elif source_type == 'HTML':
            pass


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
        stamp = self.get_date_time() + id + '_' + post
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

    def filter_word_(self, word):
        word = re.sub('\\d', "", word)
        word = re.sub('사용', "", word)
        return word

    def scrap(self, text):
        startTime = time.time()
        self.save_txt(text)
        output = {}

        for p in text:
            # print(p)
            p = self.clean_word(p)
            if len(p) < 2:
                continue

            pp = self.k.nouns(p)
            pp = list(map(lambda x: self.clean_word(x), pp))
            pp = list(filter(lambda x: self.filter_word(x), pp))
            # print('after text : ', text)
            pp = list(filter((lambda x: len(x) >= 2), pp))

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
        self.save_kor_db(data)


        # print(content)


if __name__ == "__main__":

    url = "http://blog.cjred.net/rss/"
    cl = KorCrawler()
    print(cl.filter_word('경우'))
    # get_rss_post_content(url)
    # set_section_id(2)