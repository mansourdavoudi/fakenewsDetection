import os.path
import networkx as nx
import shutil
from networkx.algorithms.traversal.depth_first_search import dfs_tree
import json
import matplotlib.pyplot as plt
import numpy as np
import math
from os.path import join
from collections import OrderedDict
from operator import itemgetter
import csv
import time
from datetime import timedelta
from datetime import datetime

def ComputeFtlr(G):
    hours=0
    datetimeFormat = "%a %b %d %H:%M:%S %Y"
    dictTweet={}
    dictRetweet={}
    for node in G.nodes(data=True):
        if(node[1]['id']==2):
            dictTweet[node[0]]=node[1]['CreatedAt']
    for node in G.nodes(data=True):
        if(node[1]['id']==3 or node[1]['id']==4):
            dictRetweet[node[0]]=node[1]['CreatedAt']
    if(len(dictTweet) > 0 and len(dictRetweet)> 0):
        sortedDictT = sorted(
            dictTweet.items(),
            key=lambda x: datetime.strptime(x[1], '%a %b %d %H:%M:%S %Y'), reverse=False
        )
        sortedDictR = sorted(
            dictRetweet.items(),
            key=lambda x: datetime.strptime(x[1], '%a %b %d %H:%M:%S %Y'), reverse=True
        )
        tw = next(iter(sortedDictT))
        rw = next(iter(sortedDictR))
        #print(tw)
        #print(rw)
        diff = datetime.strptime(rw[1], datetimeFormat) - datetime.strptime(tw[1], datetimeFormat)
        hours = (diff.days) * 24 + (diff.seconds) / 3600

    return hours

Path_Fake= "C:\dataset\Politifact\\real_trees"

#G=nx.read_gpickle("C:\dataset\Politifact\Graphs\\news politifact11773.gpickle")
li={}
p=[]
c=0
for news in os.listdir(Path_Fake):
    print("news --->" , news,"\n")
    G = nx.read_gpickle(join(Path_Fake,news))
    h=ComputeFtlr(G)
    if(h<24):
        print(news,"-> deleted")
        li=news.split(" ")
        n=li[1]
        n=n.replace(".gpickle","")
        os.chdir("C:\dataset\Politifact\politifact_real_temp")
        shutil.rmtree(n)
        print(n,"removed")



