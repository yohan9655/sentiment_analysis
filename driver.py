#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 18:54:55 2022

@author: yohan
"""
import argparse

import scrapper
import sentiment_analyser
import os


def main(args):
    if args.g.lower() == 'false' and args.n != None:
        print('args.g cannot be False when args.n value is set')
    else:
        if (args.g.lower() == 'true' or len([name for name in os.listdir('./articles') 
                                   if os.path.isfile('./articles/' + name)]) != args.n):
            list_links = scrapper.get_articles(args.n)
            scrapper.to_json(list_links)
            
        if args.n >= 3:
            articles = ['1<sup>st</sup>','2<sup>nd</sup>','3<sup>rd</sup>']
            articles1 = [str(i)+'<sup>th</sup>' for i in range(4,args.n+1)]
            articles = articles + articles1
        elif args.n==2:
            articles = ['1<sup>st</sup>','2<sup>nd</sup>']
        elif args.n == 1:
            articles = ['1<sup>st</sup>']
            
        list_articles = sentiment_analyser.pre_process(args.n)
        if args.x == None and args.y == None:
            results_flair = sentiment_analyser.calculate_sentiment_flair(list_articles, args.n)
            results_nltk = sentiment_analyser.calculate_sentiment_nltk(list_articles, args.n)
            sentiment_analyser.graph_flair(articles, results_flair)
            sentiment_analyser.graph_nltk(articles, results_nltk)
            
        elif args.x.lower() == 'flair':
            results_flair = sentiment_analyser.calculate_sentiment_flair(list_articles, args.n)
            sentiment_analyser.graph_flair(articles, results_flair)
            if args.y != None and args.y.lower() == 'nltk':
                results_nltk = sentiment_analyser.calculate_sentiment_nltk(list_articles, args.n)
                sentiment_analyser.graph_nltk(articles, results_nltk)
        elif args.x.lower() == 'nltk':
            results_nltk = sentiment_analyser.calculate_sentiment_nltk(list_articles, args.n)
            sentiment_analyser.graph_nltk(articles, results_nltk)
            if args.y != None and args.y.lower() == 'flair':
                results_flair = sentiment_analyser.calculate_sentiment_flair(list_articles, args.n)
                sentiment_analyser.graph_flair(articles, results_flair)
        else:
            print('Enter valid argument. For both flair and nltk,'
                  'leave argument empty or type both nltk and flair.'
                      ' For any one, type nltk or flair.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', nargs = '?', default = 'false', type = str, required=False)
    parser.add_argument("-n", nargs = '?', default = 10, type = int, required=False)
    parser.add_argument('x', nargs = '?', default = None, type = str)
    parser.add_argument("y", nargs = '?', default = None, type = str)
    
    args = parser.parse_args()
    print(args.g)
    main(args)
    