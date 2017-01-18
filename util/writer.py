import csv
import logging

logger = logging.getLogger()
def save_csv(data, fileName):
    # with 문을 사용하면 with 블록을 벗어나면 파일 객체 f 가 자동으로 close 되어 편리하다.
    logger.info("CSV format save : %s", fileName)
    with open(fileName, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for word, freq in data:
            writer.writerow([word, freq])


def save_txt(data, fileName):
    logger.info("TXT format save : %s", fileName)
    with open(fileName, 'w') as f:
        for p in data:
            f.write(p + "\n")


if __name__ == "__main__":
    data = [('nbs2', 11), ('Selenium', 4), ]
    #save_eng_db(data, 1)

