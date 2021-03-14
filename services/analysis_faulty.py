import codecs
import re
import os
import glob
from typing import Any, Dict, List, Text
from pyvi import ViTokenizer, ViPosTagger
from tensorflow.keras.preprocessing.text import Tokenizer

class AnalysisFaulty:
    
    @staticmethod
    def generateMap(words):
        bi_grams = []
        for word in words:
            bi_grams.append(word.lower())
        return bi_grams

    @staticmethod
    def tokenize(string: str):
        tokenized = ViTokenizer.tokenize(string)
        words, label = ViPosTagger.postagging(tokenized)

        for idx, word in enumerate(words):
            word = word.replace('_', " ")
            words[idx] = word

        words = [w for w in words if w]

        return words

    @staticmethod  
    def map_with_faulty_file(bi_grams):
        folders = glob.glob(os.path.join(os.path.dirname(__file__), 'data/*.txt'))
        
        map_with_faulty = {}
        for folder in folders:
            folderArr = folder.split('\\')
            faultyTxt = folderArr[len(folderArr) - 1]
            faulty = faultyTxt.split('.')[0]
            map_with_faulty[faulty] = AnalysisFaulty.get_faulty_file(folder, bi_grams)
        
        return map_with_faulty

    @staticmethod
    def get_faulty_file(path_file, words):
        grams = {}

        for word in words:
            removeSpaceWord = word.replace(" ", "")
            lowerString = removeSpaceWord.lower()
            grams[lowerString]=1

        with codecs.open(os.path.join(os.path.dirname(__file__), path_file), 'r', encoding='utf-8') as fin:
            for token in fin.read().split('\n'):
                token = token.replace('\r', '')
                removeSpaceWord = token.replace(" ", "")
                word = removeSpaceWord.lower()
                if word in grams:
                    grams[word]+=1
                else: 
                    grams[word]=1

        return grams

    @staticmethod
    def compute_confidence(wordsObject):
        count = 0          
        for word, value in wordsObject.items():
            if value >= 2:
                count+=1

        return count/len(wordsObject.items())

# words = AnalysisFaulty.tokenize(u"Hình thức tuyển sinh tại trường. Bạn sẽ nộp hồ sơ tại trường")
# print("word", words)
# objectFaulty = AnalysisFaulty.map_with_faulty_file(words)
# print("objectFaulty", objectFaulty)

# for faulty, value in objectFaulty.items():
#     print("faulty", faulty)
#     print("value", value)
#     print("compute_confidence", AnalysisFaulty.compute_confidence(value))