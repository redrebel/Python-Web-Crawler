from nltk import word_tokenize, sent_tokenize
from nltk import pos_tag
import operator
import time
import logging
import re
from Scraping import Scraping
from util import writer

logger = logging.getLogger()


def getwords(txt):
    '''
    단순히 문자열을 단어별로 나눈다.
    :param txt:
    :return:
    '''
    # print(txt)
    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    # Convert to lowercase
    return [word.lower() for word in words if word not in ['', 'time']]


class EngCrawler(Scraping):

    def __init__(self):
        self.set_filter_words('source_list/ENG/ENG_filterwords.txt')

    # Return title and dictionary of word counts for an RSS feed

    def proc(self, section_id, source_type, source_list):
        print('section_id : ', section_id, ", file_path : ", source_list)
        self.set_section_id(section_id)
        startTime = time.time()
        if source_type == 'RSS':
            self.proc_list(source_list, type=self.get_feed_post_content)
        elif source_type == 'EGLOOS':
            self.get_egloos_post_content("lennis", "6072774")
        elif source_type == 'TEXT':
            self.proc_list(source_list, type=self.proc_text_content)
        elif source_type == 'HTML':
            pass

        checkTime = time.time() - startTime
        logger.debug("work time : %f", checkTime)

    def scrap_(self, text):
        '''
        일반적으로 단어로 쪼개서 처리한다
        :param text:
        :return:
        '''
        txt = [text.feed.title]
        wc = {}
        # Loop over all the entries
        i = 0
        for e in text.entries:
            if 'content' in e:
                print('content : ', e.content)
                content = e.content[0].get('value')
            elif 'description' in e:
                print('description')
                content = e.description
            else:
                print('summary')
                content = e.summary
            i += 1
            # print e
            # Extract a list of words
            # Remove all the HTML tags
            # print('before txt : ', content)
            content = re.compile(r'<[^>]+>').sub('', content)
            content = content.strip()
            # content = re.sub(' +', '', content)
            print('after : [', content,']')
            txt.append(content)
            # content = self.clearInput(content)

            words = getwords(e.title + ' ' + content)
            for word in words:
                # print word
                wc.setdefault(word, 0)
                wc[word] += 1
        writer.save_txt(txt, self.save_file_path+self.save_file_name+".txt")
        print('i : ', i, " txt : ", text)
        count = sorted(wc.items(), key=operator.itemgetter(1), reverse=True)
        print(text.feed.title, count)
        writer.save_eng_db(count, self.section_id)


    def scrap(self, text):
        '''
        자연어처리를 통하여 명사만 처리한다
        :param text:
        :return:
        '''
        self.save_txt(text)
        nouns = ['NN', 'NNS', 'NNP', 'NNPS']

        output = {}
        # Loop over all the entries
        for content in text:

            # txt.append(content)
            # content = self.clearInput(content)
            sentences = sent_tokenize(content)
            for sentence in sentences:
                # print(sentence)
                taggedWords = pos_tag(word_tokenize(sentence))

                for word in taggedWords:
                    keyword = word[0].lower()
                    tag = word[1]
                    if tag in nouns and self.filter_word(keyword):

                        # print(temp)
                        if keyword not in output:
                            output[keyword] = 0
                        output[keyword] += 1

        #print(text[0], output)
        output = self.get_sorted_data(output)
        self.save_csv(output)
        self.save_eng_db(output)


def main():
    cl = EngCrawler()
    cl.proc(1, 'ddd')

if __name__ == "__main__":
    main()