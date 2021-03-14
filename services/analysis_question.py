import codecs
import re
import os
import glob
from typing import Any, Dict, List, Text
from pyvi import ViTokenizer, ViPosTagger
from tensorflow.keras.preprocessing.text import Tokenizer

class AnalysisQuestion:

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
    def get_question_file(words):
        grams = {}

        for word in words:
            removeSpaceWord = word.replace(" ", "")
            lowerString = removeSpaceWord.lower()
            grams[lowerString]=1

        with codecs.open(os.path.join(os.path.dirname(__file__), 'datatype/question_type.txt'), 'r', encoding='utf-8') as fin:
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