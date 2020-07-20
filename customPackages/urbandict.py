#!/usr/bin/env python
#
# Simple interface to urbandictionary.com
#
# Author: Roman Bogorodskiy <bogorodskiy@gmail.com>

import requests
from bs4 import BeautifulSoup

class WordBlock:
    def __init__(self,word,meaning,example):
        self.word = word
        self.meaning = meaning
        self.example = example
    
class UrbanDic:
    def __init__(self):
        pass
    
    def initNewWord(self,word):
        self.word = word
        self.url = f"http://www.urbandictionary.com/define.php?term={self.word}"
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        
    def define(self,word):
        try:
            self.initNewWord(word)
        except Exception:
            print(f"Error finding {self.word} on Urban Dictionary")
            return None
        
        wordBlocks = self.soup.find_all(class_='def-panel')
        
        words = []
        meanings = []
        examples = []
        for block in wordBlocks:
            words.append(block.find(class_ = 'word').get_text())
            meanings.append(block.find(class_ = 'meaning').get_text()) 
            examples.append(block.find(class_ = 'example').get_text())
            #examples.append([])
        
        wordBlocks = []
        for i,word in enumerate(words):
            wordBlocks.append(WordBlock(words[i],meanings[i],examples[i]))

        return wordBlocks
            
        