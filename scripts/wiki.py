from __future__ import print_function
import six
from gensim.corpora import WikiCorpus

if __name__ == '__main__':
    inp = "/home/intsig/Downloads/enwiki-20190420-pages-articles-multistream3.xml-p88445p200507.bz2"
    outp = "/home/intsig/experiment/exp1_multimodal_FCN/deconv/pdf_generate_latex/doc/out_wiki.en.txt"
    space = " "
    i = 0

    output = open(outp, 'w', encoding="utf-8")
    wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        print(i)
        if((i+1) % 30000 == 0):
            print(i)
            break
        if six.PY3:
            output.write(' '.join(text) + '\n')
        else:
            output.write(space.join(text) + "\n")
        i = i + 1
    output.close()