# coding=utf-8

import json
import subprocess
import time
import requests
import sys
import re
from collections import OrderedDict
import matplotlib.pyplot as plt
from pprint import pprint
from bs4 import BeautifulSoup
from wordcloud import WordCloud

reload(sys)
sys.setdefaultencoding('utf8')

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = sys.argv[1]

def word_count(str):
	counts = dict()
	words = str.split()
	
	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	return counts

text = ""	
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
tracks = pageSoup.find_all("ul", {"class": "tracks"})
tracks = tracks[0].findChildren('li')

for a in tracks:
	song = a.findChildren('a')[0]['href']
	pageSong ="https://www.vagalume.com.br" + song
	pageTree = requests.get(pageSong, headers=headers)
	pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
	songLyrics = pageSoup.find_all("div", {"itemprop": "description"})
	lyrics = " ".join(item.strip() for item in songLyrics[0].find_all(text=True))
	text = lyrics + " " + text

# Remove charecters specials

text = text.lower()
text = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', ' ', text)
# Remove words when length less tree
words_remove = ['a','que', 'de','oi','eu', 'um', 'vem', 'do', 'da', 'vai', 'na', 'no', 'e', 'tu', 'to', 'ta', 'se', 'uma', 'não', 'sim', 'meu', 'seu', 'nos', 'pra', 'tudo', 'só', 'sua','para', 'está', 'esta', 'por', 'ao', 'os', 'foi', 'mas', 'como', 'vou', 'ele', 'mim', 'ia', 'assim', 'muito', 'já', 'há', 'tua', 'onde', 'mais', 'sem', 'teu', 'em', 'dos', 'mesmo', 'tão', 'esses', 'suas', 'ti', 'seus', 'então', 'sou', 'ser', 'minha', 'sei', 'deu', 'todo', 'te', 'será', 'até', 'faz', 'são']
for i in words_remove:
	text = re.sub(r'\s'+i+'([\s,\.])',r'\1',text) 
#text = re.sub(r'\b\w{1,3}\b', ' ', text)

count =  word_count(text)
print(sorted(count.items(), key=lambda kv: kv[1], reverse=True))

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
# lower max_font_size
wordcloud = WordCloud(max_font_size=60).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
