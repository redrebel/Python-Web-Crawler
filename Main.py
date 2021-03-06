import logging
import os
import os.path
import configparser
import time
from db import dao
from eng_crawler import EngCrawler
from kor_crawler import KorCrawler
from config import Config

logger = logging.getLogger()
stamp = "0000"
DEFAULT_LOG_PATH = "logs/"


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
    stamp = time.strftime("%Y%m%d", time.localtime())
    file_handler = logging.FileHandler("logs/scraping."+stamp+".log")
    stream_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def get_source_list(file_path):
    source_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line[0] != '#' and line != '\n':
                source_list.append(line.strip())
    return source_list


def main():
    set_time_based_stamp()
    set_logger()

    Config.load('config.conf')
    section_id = dao.get_section_id(Config.section)
    source_list = get_source_list(Config.file_path)
    logger.info('Crawling Start! mode : %s\n', Config.mode)
    start_timestamp = time.time()
    if Config.mode == 'KOR':
        cl = KorCrawler()
        cl.proc(section_id, Config.source_type, source_list)
    elif Config.mode == 'ENG':
        cl = EngCrawler()
        cl.proc(section_id, Config.source_type, source_list)
    else:
        print('unknown language.')

    work_time = time.time() - start_timestamp
    logger.info("Work Time is : %f", work_time)


if __name__ == "__main__":
    main()
