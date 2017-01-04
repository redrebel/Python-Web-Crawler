import logging
import pymysql
import configparser

logger = logging.getLogger()
config = configparser.ConfigParser()
config.read('config.conf')

db = 'DB'
DB_HOST = config.get(db, 'host')
DB_PORT = config.get(db, 'port')
DB_USER_ID = config.get(db, 'user_id')
DB_PASSWORD = config.get(db, 'password')
DB_CHARSET = config.get(db, 'charset')


def get_section_id(section):
    conn = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER_ID, passwd=DB_PASSWORD, charset='utf8')
    cur = conn.cursor()
    cur.execute('USE scraping')
    sql = "SELECT id FROM sections WHERE section = %s"
    section_id = None
    try:
        cur.execute(sql, section)
        section_id = cur.fetchone()[0]
    except Exception as e:
        logger.error("error : ", str(e))
    finally:
        cur.close()
        conn.close()
    return section_id

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
                # logger.debug('Insert Keyword')
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
        logger.debug('DB save OK')
    except Exception as e:
        logger.error("error : ", str(e))
        # Rollback in case there is any error
        conn.rollback()

    finally:
        cur.close()
        conn.close()


