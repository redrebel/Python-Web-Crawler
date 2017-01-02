import csv
import pymysql
import configparser
import logging

logger = logging.getLogger()
config = configparser.ConfigParser()
config.read('config.conf')

db = 'DB'
DB_HOST = config.get(db, 'host')
DB_PORT = config.get(db, 'port')
DB_USER_ID = config.get(db, 'user_id')
DB_PASSWORD = config.get(db, 'password')
DB_CHARSET = config.get(db, 'charset')
print(DB_CHARSET)


def save_db(data, section_id, lang):
    if lang == 'ENG':
        keyword_tb = 'eng_keywords'
        cnt_tb = 'eng_cnts'
    elif lang == 'KOR':
        keyword_tb = 'keywords'
        cnt_tb = 'cnts'
    conn = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER_ID, passwd=DB_PASSWORD, charset='utf8')
    cur = conn.cursor()
    cur.execute('USE scraping')

    try:
        for keyword, cnt in data:
            # print(keyword, cnt, sep=':')

            sql = "SELECT id FROM " + keyword_tb + " WHERE keyword=%s"
            cur.execute(sql, keyword)
            keyword_id = cur.fetchone()
            if keyword_id is None:
                logger.debug('Insert Keyword')
                # print('Insert Keyword')
                sql = "INSERT INTO " + keyword_tb + "(keyword) values(%s)"
                cur.execute(sql, keyword)
                sql = "SELECT id FROM " + keyword_tb + " WHERE keyword=%s"
                cur.execute(sql, keyword)
                keyword_id = cur.fetchone()

            sql = "INSERT INTO " + cnt_tb + "(keyword_id, section_id, cnt)"
            sql += "  VALUES(%s, %s, %s) "
            sql += "ON DUPLICATE KEY "
            sql += "UPDATE cnt=cnt+%s"

            cur.execute(sql, (keyword_id, section_id, cnt, cnt))

        conn.commit()
    except Exception as e:
        print("error : ", str(e))
        # Rollback in case there is any error
        conn.rollback()

    finally:
        cur.close()
        conn.close()


def save_eng_db(data, section_id):
    save_db(data, section_id, 'ENG')

def save_csv(data, fileName):
    # with 문을 사용하면 with 블록을 벗어나면 파일 객체 f 가 자동으로 close 되어 편리하다.
    print("CSV format save : ", fileName)
    with open(fileName, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for word, freq in data:
            writer.writerow([word, freq])


def save_txt(data, fileName):
    print("TXT format save : ", fileName)
    with open(fileName, 'w') as f:
        for p in data:
            f.write(p + "\n")


if __name__ == "__main__":
    data = [('nbs2', 11), ('Selenium', 4), ]
    save_eng_db(data, 1)

