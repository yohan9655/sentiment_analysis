#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 22:57:42 2022

@author: yohan
"""

import json
from flair.models import TextClassifier
from flair.data import Sentence
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer

import plotly.express as px
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import argparse
#pio.renderers.default='svg'

def pre_process(n: int):
    list_articles = []
    for i in range(n):
        data_req = {}
        with open('articles/' + str(i) + '.json', 'r') as f:
          data = json.load(f)
        data_req['Title'] = data['Title']
        data_req['Body'] = data['Body']
        list_articles.append(data_req)
    return list_articles


def calculate_sentiment_flair(list_articles: list, n: int):
    results_flair = []
    classifier = TextClassifier.load('sentiment')
    progress_bar = tqdm(range(n))
      
    for i in progress_bar:
        progress_bar.set_description("Flair: Processing %ith Article" % (i+1))
        data = list_articles[i]
        sen = data['Body']
        sen_title = data['Title']
        sentence_body_flair = Sentence(sen)
        sentence_title_flair = Sentence(sen_title)
          
        classifier.predict(sentence_body_flair)
        classifier.predict(sentence_title_flair)
        
        value = sentence_body_flair.tag
        value_title = sentence_title_flair.tag
        if value == 'POSITIVE':
            score_body_flair = sentence_body_flair.score
        else:
            score_body_flair = -1*sentence_body_flair.score
          
        if value == 'POSITIVE':
            score_title_flair = sentence_title_flair.score
        else:
            score_title_flair = -1*sentence_title_flair.score
              
        results_flair.append(0.6*score_body_flair + 0.4*score_title_flair)
    return results_flair


def calculate_sentiment_nltk(list_articles: list, n: int):
    sia = SentimentIntensityAnalyzer()
    progress_bar = tqdm(range(n))
    results_nltk = []
      
    for i in progress_bar:
        progress_bar.set_description("NLTK: Processing %ith Article" % (i+1))
        data = list_articles[i]
        sen = data['Body']
        sen_title = data['Title']
          
        score_nltk_body = list(sia.polarity_scores(sen).values())
        score_nltk_title = list(sia.polarity_scores(sen_title).values())
        score_nltk = [score_nltk_body[i]*0.6 + score_nltk_title[i]*0.4 
                      for i in range(4)]
        results_nltk.append(score_nltk)
    return results_nltk


def graph_flair(articles: list, results_flair: list):
    data = pd.DataFrame()
    data['Articles'] = articles
    data['sentiment'] = results_flair
    state = [0 if i > 0 else 1 for i in results_flair]
    data['state'] = state
    fig = px.bar(data, x = 'Articles', y = 'sentiment', text_auto='.3f',
                 title = 'Flair')
    fig.update_traces(textfont_size=10, textangle=0, textposition="outside",
                      cliponaxis=False)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()
    fig.write_image("graphs/fig1.png", scale = 4)


def graph_nltk(articles: list, results_nltk: list):
    data = pd.DataFrame()
    data['Articles'] = articles
    data['Negative'] = [i[0] for i in results_nltk]
    data['Neutral'] = [i[1] for i in results_nltk]
    data['Positive'] = [i[2] for i in results_nltk]
    fig = px.bar(data, x="Articles", y=["Negative", "Neutral", "Positive"],
                 title="NLTK", text_auto='.3f')
    fig.update_traces(textfont_size=10, textangle=0, textposition="outside",
                      cliponaxis=False)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()
    fig.write_image("graphs/fig2.png", scale = 4)
    
    data = pd.DataFrame()
    data['Articles'] = articles
    data['Objectivity-Subjectivity'] = [i[3] for i in results_nltk]
    fig = px.bar(data, x="Articles", y='Objectivity-Subjectivity',
                 title="Objectivity-Subjectivity Score", text_auto='.3f')
    fig.update_traces(textfont_size=10, textangle=0, textposition="outside",
                      cliponaxis=False)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()
    fig.write_image("graphs/fig3.png", scale = 4)
 
