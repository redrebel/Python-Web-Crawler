from nltk import word_tokenize, sent_tokenize
from nltk import pos_tag
import operator


class EngCrawler:

    def proc(self, section_id, file_path):
        print('section_id : ', section_id, ", file_path : ", file_path)
        doc_en = "For projects that support research infrastructure and tools, such as vessels, facilities, and telescopes, the project/performance site should correspond to the physical location of the research asset. For research assets or projects that are geographically distributed, the proposer should report information for the primary site, as defined by the proposer. For example, proposals for the operations and maintenance of research vessels may list the project/performance site as the vessel’s home port."
        tokens = word_tokenize(doc_en)
        tags_en = pos_tag(tokens)
        print(tags_en)

        sentences = sent_tokenize(doc_en);
        nouns = ['NN', 'NNS', 'NNP', 'NNPS']
        output = {}
        for sentence in sentences:
            print(sentence)
            taggedWords = pos_tag(word_tokenize(sentence))
            for word in taggedWords:
                if word[1] in nouns:
                    temp = word[0]
                    print(temp)
                    if temp not in output:
                        output[temp] = 0
                    output[temp] += 1

        print(output)
        count = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
        print("count :", count)
        for word, freq in count:
            print(word, freq)


def main():
    cl = EngCrawler()
    cl.proc(1, 'ddd')

if __name__ == "__main__":
    main()