#!/usr/bin/env python
#
# Simple interface to urbandictionary.com
#
# Author: Roman Bogorodskiy <bogorodskiy@gmail.com>

import requests
from bs4 import BeautifulSoup

class WordBlock:
    def __init__(self,word,meaning,example,ribbon = None):
        self.word = word
        self.meaning = meaning
        self.example = example
        self.ribbon = ribbon
    
class UrbanDic:
    def __init__(self):
        pass
    
    def formatSearchTerm(self,term):
        return '%20'.join(term.split())

    def define(self,word):
        try:
            word = ' '.join(word.split())
            url = f"http://www.urbandictionary.com/define.php?term={self.formatSearchTerm(word)}"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
        except Exception:
            print(f"Error finding '{word}' on Urban Dictionary")
            return None
        
        wordBlocks = soup.find_all(class_='def-panel')
        
        words = []
        meanings = []
        examples = []
        for block in wordBlocks:
            if 'word of the day' not in block.find(class_ = 'ribbon').get_text().lower(): #remove word of the day from meaning list
                words.append(block.find(class_ = 'word').get_text())
                meanings.append(block.find(class_ = 'meaning').get_text()) 
                examples.append(block.find(class_ = 'example').get_text())

        
        wordBlocks = []
        for word,meaning,example in zip(words,meanings,examples):
            wordBlocks.append(WordBlock(word,meaning,example))
        
        return wordBlocks

    def WOTD(self):
        try:
            url = 'https://www.urbandictionary.com/'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
        except Exception:
            print(f'Error finding Word of the Day')
        
        wotdBlock = soup.find(class_='def-panel')
        
        word = wotdBlock.find(class_ = 'word').get_text()
        meaning = wotdBlock.find(class_ = 'meaning').get_text()
        example = wotdBlock.find(class_ = 'example').get_text()
        ribbon = wotdBlock.find(class_ = 'ribbon').get_text()
        
        return WordBlock(word,meaning,example,ribbon)
        
             