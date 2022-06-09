#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:42:14 2022

@author: yohan
"""
import requests
import json
from tqdm import tqdm

from bs4 import BeautifulSoup

URL = 'https://www.aljazeera.com/where/mozambique/'

#This method will visit the main link and find articles.
def get_articles(max_count):
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    list_links = []
    count = 0
    itr = soup.select('article[class *= "gc u-clickable-card gc--type-post"] a')
    progress_bar = tqdm(itr)
    for link in progress_bar:
        progress_bar.set_description("Getting URLs of Articles")
        if count == max_count:
            print('Number of articles needed satisfied. Stopping Loop')
            break
        count +=1
        list_links.append('https://www.aljazeera.com' + link.get('href'))
        
    return list_links


# This method will visit all the articles found in the getArticle method 
# and store the article information in json files.
# The json file will contain the URL, Title, Date, Body, and the Source.
def to_json(list_links):
    progress_bar = tqdm(list_links)
    for ind, url in enumerate(progress_bar):
        progress_bar.set_description("Processing %ith Article" % (ind+1))
        f = open('articles/' + str(ind) + '.json','w+')
        article_url = requests.get(url)
        soup_article = BeautifulSoup(article_url.text, 'html.parser')
        para = soup_article.select('main p')
        text = ''
        dict_article = {}
        for p in para:
            text = text + '\n' + p.text
        dict_article['URL'] = url
        dict_article['Title'] = soup_article.title.text
        dict_article['Date'] = soup_article.find("span", 
                                                 {"aria-hidden" : "true"}).text
        dict_article['Body'] = text
        dict_article['Source'] = soup_article.find("div", {"class" : 
                                                   "article-source"}).text[8:]
        json.dump(dict_article, f)
        f.close()
    print('\nArticles have been saved in .json format')
  