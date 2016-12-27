import logging
import Scraping
import os
import os.path
import configparser

from konlpy.tag import Hannanum
from konlpy.utils import pprint
from konlpy.tag import Kkma
import time

logger = logging.getLogger()
stamp = "0000"
DEFAULT_LOG_PATH = "logs/"
COMPUTER_SECTION = "COMPUTER"
FASION_SECTION = "FASION"
DEFAULT_SCRAPING_SECTION = COMPUTER_SECTION


def set_time_based_stamp():
    global stamp
    stamp = time.strftime("%Y%m%d%I%M", time.localtime())
    print(stamp)


def set_logger():
    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    # logging.basicConfig(filename="log.log", level=logging.DEBUG)
    global logger
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    fileHandler = logging.FileHandler("logs/scraping.sql."+stamp+".log")
    streamHandler = logging.StreamHandler()

    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)


def get_nlpy():
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


def get_section_idx(section):
    """
    나중에 DB와 연동하여 세션아이디를 가져오는것으로 수정예정
    """
    section_idx = 0
    section_map = {"COMPUTER":1, "FASION":2}
    section_idx = section_map.get(section)
    return section_idx


def get_feed_list():
    with open("feed/feedlist.txt", 'r') as f:
        feed_list = f.readlines()
    return feed_list

# http://api.egloos.com/lennis/post/6072774.xml


def proc_kor(section_idx):
    k = get_nlpy()
    Scraping.set_knlpy(k)
    # Scraping.set_stamp(stamp)
    Scraping.set_section_idx(section_idx)

    feed_list = get_feed_list()
    Scraping.proc_feed_list(feed_list)
    # Scraping.get_rss_post_content(k, "http://blog.cjred.net/rss/")
    # Scraping.get_egloos_post_content("lennis", "6072774")


def proc_eng(section_idx):
    print(section_idx)


def main():
    set_time_based_stamp()
    set_logger()

    config = configparser.ConfigParser()
    config.read('config.conf')

    mode = config.get('Default', 'mode')
    section = config.get('Default', 'section')
    section_idx = get_section_idx(section)

    print('mode : ', mode)
    if mode == 'KOR':
        proc_kor(section_idx)
    elif mode == 'ENG':
        proc_eng(section_idx)
    else:
        print('unknown language.')


if __name__ == "__main__":
    main()
