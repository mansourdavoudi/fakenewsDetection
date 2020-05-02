import os.path
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import OrderedDict
from operator import itemgetter
import csv


Path_Fake="C:\dataset\Politifact\politifact_real"

analyser = SentimentIntensityAnalyzer()

def PEngage(id,data,G):
    if ('tweet_replies' in data):
        for i in range(len(data['tweet_replies'])):
            temp=data['tweet_replies'][i]
            pid = temp['id']
            sentence=temp['text']
            score=sentiment_analyzer_scores(sentence)
            s=score['compound']
            G.add_node(pid,score=s)
            if('engagement' in temp ):
                PEngage(pid,temp['engagement'],G)

def sentiment_analyzer_scores(sentence):

    score = analyser.polarity_scores(sentence)
    return score

def add_edge(G):
        n_list=list(G.nodes(data=True))
        for i in range (len(n_list)):
            score = n_list[i][1]['score']
            for j in range(len(n_list)):
                s = n_list[j][1]['score']
                if i!=j and nodes_connected(n_list[i][0],n_list[j][0])==False and abs(score-s) < .5:
                    G.add_edge(n_list[i][0],n_list[j][0],weight=1/(abs(score-s)+.01))

def nodes_connected(u, v):
    return u in G.neighbors(v)

co=0
for news in os.listdir(Path_Fake):
    print( "news --->" , news,"\n")
    root=str(news)
    G = nx.Graph()
    path=Path_Fake+"\\"+news
    os.chdir(path)
    with open ('tweets.json') as TwFile:
        data=json.load(TwFile)
        ids=[]
        for i in range(len(data['tweets'])):
            id = data['tweets'][i]['tweet_id']
            ids.append(id)
    with open ('replies.json',encoding="utf8") as PeFile:
        pdata=json.load(PeFile)
        for i in range(len(ids)):
            index = str(ids[i])
            if (len(pdata[index]) != 0 ):
                for j in range(len(pdata[index])):
                    temp=pdata[index][j]
                    pid=temp['id']
                    sentence=temp['text']
                    score=sentiment_analyzer_scores(sentence)
                    s=score['compound']
                    G.add_node(pid,score=s)
                    if ('engagement' in temp):
                           PEngage(pid,temp['engagement'],G)
    if(len(G.nodes())>20):
        add_edge(G)
        nx.write_gpickle(G, "C:\\Users\\mansour\Desktop\\politifact_real_reply\\news %s.gpickle" % str(root))
