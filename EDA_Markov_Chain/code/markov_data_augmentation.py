# coding=utf-8

import numpy as np
import random
import jieba
import pandas as pd
from collections import Counter
random.seed(44)

def main():
    toutiao_markov_augmentation("tnews/toutiao_category_train.txt", "tnews/aug_train.txt")
    print("done.")


def toutiao_markov_augmentation(in_file, out_file):
    dat = pd.read_csv(in_file, sep="_!_", header=None, names=["news_id", "label", "classname", "title", "keywords"])
    print(f"num train samples: {len(dat)}")
    dat = dat[:100]
    lbl2cls = {x:y for x,y in dat[["label", "classname"]].drop_duplicates().values}
    print(f"num class: {len(lbl2cls)}")
    x_train, y_train = dat["title"].apply(lambda x: " ".join([w for w in jieba.cut(x, cut_all=False)]).strip()), dat["label"]
    c = Counter(x_train.apply(lambda x: len(x.split())))
    lenghts = np.asarray(list(c.keys()))
    freq = np.asarray(list(c.values()))
    freq = freq/freq.sum()
    new_corpus, new_labels = Generator(x_train, y_train, lenghts, freq, 10, concat=False, seed=33)
    with open(out_file, "w") as fout:
        for i in range(len(new_corpus)):
            fout.write("\t".join([lbl2cls[new_labels[i]], new_corpus[i]])+"\n")
    print(f"save output to {out_file}")


### DEFINE MARKOV CHAIN GENERATOR ###

def build_chain(texts):
    
    index = 1
    chain = {}
    
    for text in texts:
        
        text = text.split()
        for word in text[index:]:
            key = text[index-1]
            if key in chain:
                chain[key].append(word)
            else:
                chain[key] = [word]
            index += 1
        
        index = 1
    
    return chain

def create_sentence(chain, lenght, seed):
    
    np.random.seed(seed)
    
    start = random.choice(list(chain.keys()))
    text = [start]

    while len(text) < lenght:
        try:
            after = random.choice(chain[start])
            start = after
            text.append(after)
        except: #end of the sentence
            #text.append('.')
            start = random.choice(list(chain.keys()))
    
    return ' '.join(text)

def Generator(x_train, y_train, lenghts, freq, rep, concat=False, seed=33):
    
    np.random.seed(seed)
    
    new_corpus, new_labels = [], []
    
    for i,lab in enumerate(np.unique(y_train)):

        selected = x_train[y_train == lab]
        chain = build_chain(selected)

        sentences = []
        for i in range(rep):
            lenght = int(np.random.choice(lenghts, 1, p=freq))
            sentences.append(create_sentence(chain, lenght, seed))

        new_corpus.extend(sentences)
        new_labels.extend([lab]*rep)
    
    if concat:
        return list(x_train) + new_corpus, list(y_train) + new_labels
    
    return new_corpus, new_labels

if __name__ == "__main__":
    main()