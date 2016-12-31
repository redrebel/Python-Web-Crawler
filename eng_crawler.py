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
    # print(txt)
    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    # Convert to lowercase
    return [word.lower() for word in words if word != '']


class EngCrawler(Scraping):
    # Return title and dictionary of word counts for an RSS feed

    def proc(self, section_id, source_type, source_list):
        print('section_id : ', section_id, ", file_path : ", source_list)
        self.set_section_id(section_id)
        startTime = time.time()
        if source_type == 'RSS':
            self.proc_feed_list(source_list)
        elif source_type == 'EGLOOS':
            self.get_egloos_post_content("lennis", "6072774")
        elif source_type == 'HTML':
            pass

        checkTime = time.time() - startTime
        logger.debug("work time : %f", checkTime)

    def scrap(self, text):
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
        # self.scrap(text)


    def scrap_nltk(self, text):
        doc_en = "For projects that support research infrastructure and tools, such as vessels, facilities, and telescopes, the project/performance site should correspond to the physical location of the research asset. For research assets or projects that are geographically distributed, the proposer should report information for the primary site, as defined by the proposer. For example, proposals for the operations and maintenance of research vessels may list the project/performance site as the vessel’s home port."
        startTime = time.time()
        text = self.clearInput(text)

        print('text : ', text)
        nouns = ['NN', 'NNS', 'NNP', 'NNPS']
        output = {}

        sentences = sent_tokenize(text);
        for sentence in sentences:
            #print(sentence)
            taggedWords = pos_tag(word_tokenize(sentence))
            for word in taggedWords:
                if word[1] in nouns:
                    temp = word[0]
                    #print(temp)
                    if temp not in output:
                        output[temp] = 0
                    output[temp] += 1

        print(output)
        count = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
        print("count :", count)
        #for word, freq in count:
        #    print(word, freq)

def main():
    cl = EngCrawler()
    cl.proc(1, 'ddd')

if __name__ == "__main__":
    main()