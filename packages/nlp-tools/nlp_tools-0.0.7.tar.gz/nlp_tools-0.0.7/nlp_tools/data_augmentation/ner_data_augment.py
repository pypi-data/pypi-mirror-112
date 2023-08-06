#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 15:18

from collections import defaultdict
import random


def get_random(start, end):
    assert start <= end - 1
    return random.randint(start, end - 1)


class NerDataAugment():
    def __init__(self, ner_json,
                 augument_size: int = 5,
                 seed: int = 0):
        random.seed(seed)
        self.ner_json = ner_json
        self.size = augument_size
        self.tag_map = self.__get_all_tag_map()

    def __get_random_ner(self, tag: str):
        assert tag in self.tag_map
        max_size = len(self.tag_map[tag])
        assert max_size > 1
        select_idx = get_random(0, max_size)
        new_sene = self.tag_map[tag][select_idx]
        return new_sene

    def __get_all_tag_map(self):
        '''
        得到目录下全部标注文件的，各种实体，ignore_tag_list 里面的不要
        :param dir_name:
        :return:
        '''
        tag_map = defaultdict(list)
        for item in self.ner_json:
            for (start, end, t_tag) in item[1]:
                tag_map[t_tag].append(item[0][start:end + 1])
        return tag_map

    def __data_augment_one(self, org_data):
        text, labels = org_data[0], org_data[1]
        new_text = ""
        new_labels = []
        current_end = 0
        for (start, end, t_tag) in labels:
            new_text += text[current_end:start]
            current_end = end+1
            new_lable_value = self.__get_random_ner(t_tag)
            new_labels.append((len(new_text),len(new_text)+len(new_lable_value)-1,t_tag))
            new_text +=new_lable_value
        return [new_text,new_labels]

    def __data_augment(self, item, size=3):
        '''
        对原始数据做增强
        :param org_data:
        :param size: 增强/最多/数量
        :return:
        '''

        new_data = []
        for i in range(size):
            new_item = self.__data_augment_one(item)
            new_data.append(new_item)
        return new_data

    def augment(self):
        '''
        对文件做增强，输出文件路径，返回size个增强好的数据对 [sentence_arr, label_arr]
        :param file_name:
        :return:
        '''
        org_data = []
        org_data += self.ner_json

        for item in self.ner_json:
            new_datas = self.__data_augment(item, self.size)
            org_data.extend(new_datas)
        return org_data


if __name__ == '__main__':
    from nlp_tools.corpus.ner.corpus_loader import ChineseDailyNerCorpus

    ccks_train = '/home/qiufengfeng/nlp/competition/天池/CCKS2021中文NLP地址要素解析/data/train.conll'
    train_data = ChineseDailyNerCorpus.load_data(ccks_train)
    NerDataAugment(train_data).augment()
    j = 1