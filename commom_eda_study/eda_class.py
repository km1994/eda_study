# @Author : King
# @Time : 2019/03/20 

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba
import synonyms
import random
from random import shuffle
random.seed(2019)
class EDA_class():
    def __init__(self,sentence,eda_type):

        # 参数配置
        self.sentence = sentence
        self.alpha = 0.2  
        # 数据增强类型调用词典；
        self.eda2fun={
            'synonym_replacement':self.synonym_replacement,
            'random_insertion':self.random_insertion,
            'random_swap':self.random_swap,
            'random_deletion':self.random_deletion
        }   
        assert eda_type in self.eda2fun,"eda_type must in {0}".format(list(self.eda2fun.keys()))
        self.eda_type = eda_type    # 数据增强类型

        # 停用词加载
        self.stop_word_path = './stopwords/stopwords.txt'
        self.stop_words = self.get_stop_word(self.stop_word_path)

        # 分词模块
        self.words,self.num_words = self.cut_word(self.sentence)
        
        # 数据增强
        new_words = self.eda2fun[self.eda_type](self.words,self.alpha,self.num_words,self.stop_words)

        print("".join(new_words))

    # 功能：同义词替换，替换一个语句中的n个单词为其同义词
    def synonym_replacement(self,words, alpha, num_words, stop_words):
        n = max(1, int(alpha * num_words))
        new_words = words.copy()
        random_word_list = list(set([word for word in words if word not in stop_words]))     
        random.shuffle(random_word_list)
        num_replaced = 0  
        for random_word in random_word_list:          
            synonyms = self.get_synonyms(random_word)
            if len(synonyms) >= 1:
                synonym = random.choice(synonyms)   
                new_words = [synonym if word == random_word else word for word in new_words]   
                num_replaced += 1
            if num_replaced >= n: 
                break

        sentence = ' '.join(new_words)
        new_words = sentence.split(' ')

        return new_words

    def get_synonyms(self,word):
        return synonyms.nearby(word)[0]

    # 功能：随机插入,随机在语句中插入n个词
    def random_insertion(self, words, alpha, num_words, stop_words):
        n = max(1, int(alpha * num_words))
        new_words = words.copy()
        for _ in range(n):
            self.add_word(new_words)
        return new_words

    def add_word(self,new_words):
        synonyms = []
        counter = 0    
        while len(synonyms) < 1:
            random_word = new_words[random.randint(0, len(new_words)-1)]
            synonyms = self.get_synonyms(random_word)
            counter += 1
            if counter >= 10:
                return
        random_synonym = random.choice(synonyms)
        random_idx = random.randint(0, len(new_words)-1)
        new_words.insert(random_idx, random_synonym)

    # 功能：随机交换：随机交货句子中的两个词
    def random_swap(self,words, alpha, num_words, stop_words):
        n = max(1, int(alpha * num_words))
        new_words = words.copy()
        for _ in range(n):
            new_words = self.swap_word(new_words)
        return new_words

    def swap_word(self,new_words):
        random_idx_1 = random.randint(0, len(new_words)-1)
        random_idx_2 = random_idx_1
        counter = 0
        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words)-1)
            counter += 1
            if counter > 3:
                return new_words
        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1] 
        return new_words

    # 功能：随机删除，以概率p删除语句中的词
    def random_deletion(self, words,  alpha, num_words, stop_words):
        if len(words) == 1:
            return words
        new_words = []
        for word in words:
            r = random.uniform(0, 1)
            if r > alpha:
                new_words.append(word)
        if len(new_words) == 0:
            rand_int = random.randint(0, len(words)-1)
            return [words[rand_int]]
        return new_words

    # 功能：分词
    def cut_word(self,sentence):
        seg_list = jieba.cut(sentence)
        seg_list = " ".join(seg_list)
        words = list(seg_list.split())
        num_words = len(words)
        return words,num_words

    # 功能：同义词加载
    def get_stop_word(self,stop_word_path):
        #停用词列表，默认使用哈工大停用词表
        f = open(stop_word_path,encoding='utf-8')
        stop_words = list()
        for stop_word in f.readlines():
            stop_words.append(stop_word[:-1])
        return stop_words

if __name__ == '__main__':
    sentence = '我们相聚在Datawhale开源组织，并一起做有意义的事情。'
    print(f"{sentence}")
    eda_class = EDA_class(sentence,'synonym_replacement')
    eda_class = EDA_class(sentence,'random_insertion')
    eda_class = EDA_class(sentence,'random_swap')
    eda_class = EDA_class(sentence,'random_deletion')