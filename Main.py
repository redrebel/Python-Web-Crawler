import logging
import Scraping
import os, os.path
from konlpy.tag import Hannanum
from konlpy.utils import pprint
from konlpy.tag import Kkma
import time

logger = logging.getLogger()

stamp = "0000"

def set_time_based_stamp():
	global stamp
	stamp = time.strftime("%Y%m%d%I%M", time.localtime())
	print(stamp)


def setLogger():
	if not os.path.exists("logs/"):
		os.makedirs("logs/")
	# logging.basicConfig(filename="log.log", level=logging.DEBUG)
	global logger
	logger.setLevel(logging.DEBUG)

	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
	fileHandler = logging.FileHandler("logs/scraping."+stamp+".log")
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


# http://api.egloos.com/lennis/post/6072774.xml
def main():
	set_time_based_stamp()
	setLogger()
	k = get_nlpy()
	Scraping.set_knlpy(k)
	Scraping.set_stamp(stamp)
	#Scraping.get_rss_post_content(k, "http://blog.cjred.net/rss/")
	Scraping.get_egloos_post_content("lennis", "6072774")

if __name__ == "__main__":
	main()
