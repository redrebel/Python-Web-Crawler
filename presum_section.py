
from nltk import word_tokenize, sent_tokenize
from nltk import pos_tag
import logging
import pymysql
import configparser
import re

logger = logging.getLogger()
config = configparser.ConfigParser()
config.read('config.conf')

db = 'DB'
DB_HOST = config.get(db, 'host')
DB_PORT = config.get(db, 'port')
DB_USER_ID = config.get(db, 'user_id')
DB_PASSWORD = config.get(db, 'password')
DB_CHARSET = config.get(db, 'charset')

filter_words = []


def filter_word(word):
    if len(word) < 2: return False
    if len(word) > 64: return False
    if bool(re.search('\\d', word)) is True: return False
    if word in filter_words: return False
    return True


def set_filter_words(file_path):
    _filter_words = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line[0] != '#' and line != '\n': _filter_words.append(line.strip())

    global filter_words
    filter_words = _filter_words
    print('filter_words : ', filter_words)


def presume(text, ):
    set_filter_words('source_list/ENG/ENG_filterwords.txt')

    output = {}
    nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    sentences = sent_tokenize(text)
    for sentence in sentences:
        # print(sentence)
        taggedWords = pos_tag(word_tokenize(sentence))

        for word in taggedWords:
            if word[1] in nouns and filter_word(word[0]):

                temp = word[0].lower()
                # print(temp)
                if temp not in output:
                    output[temp] = 0
                output[temp] += 1
    print(output)
    s1 = sum_cnts(1, output)
    s2 = sum_cnts(2, output)

    section_id = 0
    if s1 == s2:
        print('Equal !!! You need to more Scrapping')
        exit()
    elif s1 > s2:
        section_id = 1
    else:
        section_id = 2

    section = get_section(section_id)
    print('입력받은 영어문장은 ', section,'(',section_id,') 분야일 것으로 추측됩니다')

    print(list(output))
    words = list(output)

    for eng_word in words:
        print(eng_word)
        find_word(section_id, eng_word)


def get_section(section_id):
    conn = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER_ID, passwd=DB_PASSWORD, charset='utf8')
    cur = conn.cursor()
    cur.execute('USE scraping')
    sql = "SELECT section FROM sections WHERE id = %s"
    section = None
    try:
        cur.execute(sql, section_id)
        section = cur.fetchone()[0]
    except Exception as e:
        logger.error("error : ", str(e))
    finally:
        cur.close()
        conn.close()
    return section

def sum_cnts(section_id, words):

    conn = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER_ID, passwd=DB_PASSWORD, charset='utf8')
    cursor = conn.cursor()
    cursor.execute('USE scraping')
    placeholder = '%s'  # For MySQL.
    placeholders = ', '.join(placeholder for unused in words)

    query = '''
                SELECT a.keyword_id, a.cnt, b.keyword
                FROM (
                  SELECT keyword_id, cnt FROM eng_cnts
                WHERE section_id = %s)  a,
                  (SELECT id,keyword FROM eng_keywords
                  WHERE keyword in (%s)) b
                WHERE a.keyword_id = b.id
                ORDER BY a.cnt DESC
                -- LIMIT 10
                ''' % ('%s', placeholders)
    # print(query)
    # print(list(words))
    s = 0
    try:
        params = [section_id,]
        #params.append(section_id)
        params.extend(words)
        cursor.execute(query, params)
        record = cursor.fetchall()

    except Exception as e:
        logger.error("error : ", str(e))
    finally:
        cursor.close()
        conn.close()


    for id, cnt, keyword in record:
        if words.get(keyword.lower()) is None:
            print(keyword, ':', id, 'is None')
            exit()
        mo = float(words.get(keyword.lower())) * 1.2
        cnt2 = cnt * mo
        s += cnt2
        print(keyword,cnt,mo, cnt2, sep=',')

    print(s)
    return s


def sim_pearson(words):

    conn = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER_ID, passwd=DB_PASSWORD, charset='utf8')
    cursor = conn.cursor()
    cursor.execute('USE scraping')

    query = '''
            SELECT keyword_id, cnt FROM eng_cnts
            WHERE section_id = %s
            -- GROUP BY section_id
            ORDER BY cnt DESC
             LIMIT 10

            '''
    cursor.execute(query, 1)
    ls1 = cursor.fetchall()
    dic1 = {}
    for id, cnt in ls1:
        print(id,cnt, sep=':')
        dic1[id]=cnt

    cursor.execute(query, 2)
    ls2 = cursor.fetchall()
    dic2 = {}
    for id, cnt in ls2:
        print(id,cnt, sep=':')
        dic2[id]=cnt

    print(dic1[176])
    print(dic1.get(176))
    return
    placeholder = '?'  # For SQLite. See DBAPI paramstyle.
    placeholders = ', '.join(placeholder for unused in words)
    query = 'SELECT keyword_id FROM students WHERE id IN (%s)' % placeholders
    cursor.execute(query, words)

    keyword_id = cursor.fetchall()

def find_word(section_id, eng_word):
    #dic.
    words = dic.get(eng_word)
    if words is None :
        print(eng_word, '는 없습니다.')
        return ''
    conn = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER_ID, passwd=DB_PASSWORD, charset='utf8')
    cursor = conn.cursor()
    cursor.execute('USE scraping')
    placeholder = '%s'  # For MySQL.
    placeholders = ', '.join(placeholder for unused in words)

    query = '''
                SELECT a.keyword_id, a.cnt, b.keyword
                FROM (
                  SELECT keyword_id, cnt FROM cnts
                WHERE section_id = %s)  a,
                  (SELECT id,keyword FROM keywords
                  WHERE keyword in (%s)) b
                WHERE a.keyword_id = b.id
                ORDER BY a.cnt DESC
                -- LIMIT 10
                ''' % ('%s', placeholders)
    # print(query)
    # print(list(words))
    s = 0
    try:
        params = [section_id,]
        #params.append(section_id)
        params.extend(words)
        cursor.execute(query, params)
        record = cursor.fetchall()

    except Exception as e:
        logger.error("error : ", str(e))
    finally:
        cursor.close()
        conn.close()

    print(record)
    if(len(record) == 0) :
        print(eng_word, '는 없습니다.')
        return ''
    print(eng_word, '는', record[0][2], '입니다.')
    return record[0][2]



dic = {}
with open('db/EngKorDictionary.txt', 'r') as f:
    for line in f.readlines():
        if line[0] != '#' and line != '\n':
            line = line.strip().split('|')
            #print(line)
            keyword = line[0]
            words = line[1].split(',')
            #print(keyword,words)
            dic[keyword] = words
            #source_list.append(line.strip())
#print(dic)
#sim_pearson("eee")
text = 'we are talking about Material for a dress. how about Velvet?'
#text = 'Bounded Context is one of the main patterns in Domain-Driven Development. It helps you work with large domain models by dividing them into different contexts. Thanks to this your domain’s objects become smaller and business logic of your application becomes easier to understand.'
#text = 'If you’re looking to boost your field photography skills, these eight clever tricks can be done with common items almost everyone has.In this video, youtuber and photographer Peter McKinnon shares eight of his favorite photography tricks he uses in the field.'
#text = '''It's been nearly a decade since the fashion blogging phenomenon first kicked off, and after a great deal of blood, sweat, tears and ripped seams, fashion bloggers are now an accepted part of the fashion establishment, seen in the front rows of major fashion shows, landing prominent ad campaigns and starring on magazine covers. Some have even launched multimillion-dollar businesses and become household names.'''
"""text = '''The world around us is changing rapidly. And as programmers, we need to stay up to date with the most recent developments. Some of the most important trends that you need to be on top of are Cloud Computing, DevOps, Machine Learning and Ethical Hacking. Machine learning refers to the part of computer science that ...
Spring Application Framework has been in action for quite a long time, and programmers have developed several conventions, usage patterns, and idioms during that time period. In this example, we will try to explain some of them and give examples to illustrate how to apply them in your projects. Let&rsquo;s begin. Table Of Contents 1. ...
This blog has&nbsp;explained the following concepts&nbsp;for serverless applications so far: Serverless FaaS with AWS Lambda and Java AWS IoT Button, Lambda and Couchbase The third blog in serverless series will explain&nbsp;how to create a simple microservice using Amazon API Gateway, AWS Lambda and&nbsp;Couchbase. Read previous blogs for more context on AWS Lambda. Amazon API Gateway ...
This post is my personal and opinionated assessment of some of the most significant developments related to software development in 2016. This is my tenth year for this annual post and my previous years&rsquo; assessment are available for 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, and 2007. As with these previous years&rsquo; assessments, this ...
In all our project, we use data classes which, by definition, contain data (fields) but no (business) logic. According to the best coding practices, a data class should preferably be immutable because immutability means thread safety. Main reference here is Joshua Bloch&rsquo;s Effective Java book; this Yegor Bugayenko&rsquo;s post is also very interesting reading. An ...
Android Internet of things called Android Things is the new OS announced by Google. This is an Android-based OS for Internet of things (IoT). If you are new to IoT, give a look at my article about what is IoT. &nbsp;As the name Android Things implies, it is a modified version of Android OS that ...
In this article we will study about Eclipse YAML Editor. For this example we will use Eclipse Luna 4.4.2. and YEdit plugin (1.0.20) which is a YAML file editor plugin. 1. Introduction Eclipse is an integrated development environment (IDE) used in computer programming, and is the most widely used Java IDE.[3] It contains a base ...
''' """
#text = 'Angular Material. Material Design components for Angular apps. '
text = 'What is an editor? An editor is, for me, the main tool I use for work. As a Language Engineer I create new languages, I use existing ones and I need different tools to work with them. I would like to be able to hack all of them together, in a customized IDE I can ...'
presume(text)

'''
find_word(1,'editor')
find_word(1,'language')
find_word(1,'tool')
find_word(1,'engineer')
find_word(1,'languages')
find_word(1,'ide')
find_word(1,'tools')
'''