import logging
import os
import os.path
import configparser
import time

from eng_crawler import EngCrawler
from kor_crawler import KorCrawler


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
    file_handler = logging.FileHandler("logs/scraping."+stamp+".log")
    stream_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def get_section_id(section):
    """
    나중에 DB와 연동하여 세션아이디를 가져오는것으로 수정예정
    """
    section_map = {"COMPUTER": 1, "FASION": 2}
    section_idx = section_map.get(section)
    return section_idx


def get_feed_list(file_path):
    with open(file_path, 'r') as f:
        feed_list = f.readlines()
    return feed_list


def proc_eng(section_idx):

    print(section_idx)


def main():
    set_time_based_stamp()
    set_logger()

    config = configparser.ConfigParser()
    config.read('config.conf')

    mode = config.get('Default', 'mode')
    section = config.get('Default', 'section')
    section_id = get_section_id(section)
    file_path = config.get(mode, 'feed_list_file')
    feed_list = get_feed_list(file_path)
    print('mode : ', mode)
    if mode == 'KOR':
        cl = KorCrawler()
        cl.proc(section_id, feed_list)
    elif mode == 'ENG':
        cl = EngCrawler()
        cl.proc(section_id, feed_list)
    else:
        print('unknown language.')


if __name__ == "__main__":
    main()
