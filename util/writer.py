import csv
import pymysql

def save_csv(data, fileName):
    # with 문을 사용하면 with 블록을 벗어나면 파일 객체 f 가 자동으로 close 되어 편리하다.
    print("CSV format save : ", fileName)
    with open(fileName, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for word, freq in data:
            writer.writerow([word, freq])


def save_txt(data, fileName):
    print("txt format save : ", fileName)
    with open(fileName, 'w') as f:
        for p in data:
            f.write(p + "\n")


CONN_STR = ""

def save_eng_db(data, section_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='MY_PASSWORD', charset='utf8')
    cur = conn.cursor()
    cur.execute('USE scraping')


    #cur.execute("SELECT * FROM eng_keywords WHERE keyword=%s", )
    # if()
    cur.close()
    conn.close()
