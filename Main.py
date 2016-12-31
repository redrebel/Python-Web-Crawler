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


def get_source_list(file_path):
    source_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line[0] != '#':
                source_list.append(line)
        # source_list = f.readlines()
    return source_list


def main():
    set_time_based_stamp()
    set_logger()

    config = configparser.ConfigParser()
    config.read('config.conf')

    default = 'Default'
    mode = config.get(default, 'mode')
    section = config.get(default, 'section')
    section_id = get_section_id(section)
    source_type = config.get(default, 'type')
    if source_type == 'RSS':
        list_file = 'feed_list_file'
    elif source_type == 'EGLOOS':
        list_file = 'egloos_list_file'
    elif source_type == 'HTML':
        list_file = 'html_list_file'
    else:
        print('Unknown source type')
        exit()

    file_path = config.get(mode, list_file)
    source_list = get_source_list(file_path)
    print('mode : ', mode)
    if mode == 'KOR':
        cl = KorCrawler()
        cl.proc(section_id, source_type, source_list)
    elif mode == 'ENG':
        cl = EngCrawler()
        cl.proc(section_id, source_type, source_list)
    else:
        print('unknown language.')


if __name__ == "__main__":
    main()
