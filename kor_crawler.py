import logging
from konlpy.tag import Hannanum
from konlpy.utils import pprint
from konlpy.tag import Kkma
import time
import Scraping


logger = logging.getLogger()


class KorCrawler:

    def get_nlpy(self):
        """
        Kkma 는 nouns() 시 단어를 한번만 표시되고 속도가 느리지만 추출결과가 깔끔하다
        Hannanum 은 nouns() 시 단어를 매번 표시되고 (빈도수체크가능) 속도가 빠르지만 추출결과가 매끄럽지 않다.
        """
        k = Kkma()
        # k = Hannanum()
        k.nouns("intial ")
        startTime = time.time()
        checkTime = time.time() - startTime
        logger.debug("intial time : %f", checkTime)
        startTime = time.time()
        return k

    def proc(self, section_id, feed_list):
        k = self.get_nlpy()
        Scraping.set_knlpy(k)
        # Scraping.set_stamp(stamp)
        Scraping.set_section_id(section_id)

        Scraping.proc_feed_list(feed_list)
        # Scraping.get_rss_post_content(k, "http://blog.cjred.net/rss/")
        # Scraping.get_egloos_post_content("lennis", "6072774")
