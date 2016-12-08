import logging
import egloosScraping
import os, os.path

def setLogger():
	if not os.path.exists("logs/"):
		os.makedirs("logs/")
	# logging.basicConfig(filename="log.log", level=logging.DEBUG)
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
	fileHandler = logging.FileHandler("logs/scraping.log")
	streamHandler = logging.StreamHandler()

	fileHandler.setFormatter(formatter)
	streamHandler.setFormatter(formatter)

	logger.addHandler(fileHandler)
	logger.addHandler(streamHandler)

def main():
	setLogger()
	egloosScraping.scrap()

if __name__ == "__main__":
	main()