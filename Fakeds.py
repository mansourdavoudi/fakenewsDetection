import os.path
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree
import json
import glob
import matplotlib.pyplot as plt
import numpy as np
from os.path import join
import math
from collections import OrderedDict
from operator import itemgetter
import csv
import time
from datetime import timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime

analyser = SentimentIntensityAnalyzer()

Path="C:\dataset\Politifact\\temp2"

datetimeFormat = "%a %b %d %H:%M:%S %Y"

interval=14

const=24

def calBaseTime(times):

    sortedDictT = sorted(
        times.items(),
        key=lambda x: datetime.strptime(x[1], '%a %b %d %H:%M:%S %Y'), reverse=False
    )
    t = next(iter(sortedDictT))
    return(t[1])

def ComputeFtlr(G):

    hours=0
    dictTweet={}
    dictRetweet={}
    for node in G.nodes(data=True):
        if(node[1]['id']==2):
            dictTweet[node[0]]=node[1]['CreatedAt']
    for node in G.nodes(data=True):
        if(node[1]['id']==3):
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
        diff = datetime.strptime(rw[1], datetimeFormat) - datetime.strptime(tw[1], datetimeFormat)
        hours = (diff.days) * 24 + (diff.seconds) / 3600

    return hours

def calTime(tid):
    ctime=""
    with open ('retweets.json') as ReFile:
        rdata=json.load(ReFile)
        if(len(rdata[tid])>0):
            ctime=rdata[tid][0]['retweeted_status']['created_at']
    return ctime

def UsrInfo(data):
    list=[]
    flag="normal"
    followers=data['followers_count']
    friends=data['friends_count']
    if(friends>0):
        result = followers / friends
        if (result > 1):
            flag = "leader"
    vfi=data['verified']
    favorit_count=data['favourites_count']
    sts_count=data['statuses_count']
    list.append(flag)
    list.append(vfi)
    list.append(favorit_count)
    list.append(sts_count)
    return list

def totalNode(G):
    tnode=len(G.nodes())-1
    return tnode

def findTtw(G):
    counter=0
    for node in G.nodes(data=True):
        if(node[1]['id']==2):
            counter+=1
    return counter

def findTrw(G):
    counter=0
    for node in G.nodes(data=True):
        if(node[1]['id']==3):
            counter+=1
    return counter

def findTrp(G):
    counter=0
    for node in G.nodes(data=True):
        if(node[1]['id']==4):
            counter+=1
    return counter

def findTws(G):
    counter=0
    for node in G.nodes(data=True):
        if (node[1]['id'] == 2):
            print(node[0])
            li = list(G.successors())
            if(len(li) == 0 ):
                counter+=1
    return counter

def NumOutDegree(G):
    dict={}
    for n in G.nodes(data=True):
        if(n[1]['id'] == 2):
            if (len(list(G.successors(n[0]))) > 0):
                sum = len(list(G.successors(n[0])))
                dict[n[0]] = sum
    return dict

def NumMaxOutStsRe(dict,max,G):
    usrSts={}
    usrSts['normal']=0
    usrSts['leader']=0
    if(max>0):
        li = list(dict.keys())[list(dict.values()).index(max)]
        Gtemp = dfs_tree(G, li)
        Gtemp.add_nodes_from((i, G.nodes[i]) for i in Gtemp.nodes)
        for node in Gtemp.nodes(data=True):
            if(node[1]['id']==3):
                if (node[1]['usrType'] == "normal"):
                    usrSts['normal'] += 1
                elif (node[1]['usrType'] == "leader"):
                    usrSts['leader'] += 1
    return usrSts

def NumEngageTwMOut(dict,max,G):
    engage=0
    if(max>0):
        li = list(dict.keys())[list(dict.values()).index(max)]
        Gtemp = dfs_tree(G, li)
        engage += len(Gtemp.nodes()) - 1
    return engage

def MaxOutDegree(dict):
    li=[]
    max=0
    for x in dict.values():
        li.append(x)
    arr=np.array(li)
    if(len(arr)>0):
        max=np.max(arr)
    return(max)

def NumVrfRe(G):
    counter=0
    for node in G.nodes(data=True):
        if(node[1]['id']==3):
            if(node[1]['user'][1]!= False):
                counter+=1
    return counter

def NumStsRe(G):
    dict={}
    dict['normal']=0
    dict['leader']=0
    for node in G.nodes(data=True):
        if(node[1]['id']==3):
            if(node[1]['user'][0]=="normal"):
                dict['normal']+=1
            elif(node[1]['user'][0]=="leader"):
                dict['leader'] += 1
    return dict

def totalHeight(G):
    finalList=[]
    finalResult=0
    for node in G.nodes(data=True):
        if (node[1]['id']==2):
            li=[]
            dict=nx.shortest_path_length(G,node[0])
            for val in dict.values():
                li.append(val)
            arr=np.array(li)
            if(len(arr)>0):
               max=np.max(arr)
               finalList.append(max)
    f_arr=np.array(finalList)
    if(len(f_arr) > 0):
       finalResult=np.max(f_arr)
    return (finalResult+1)

def calFrequency(G):
    hours = 0
    dictEngage = {}
    for node in G.nodes(data=True):
        if (node[1]['id'] != 1):
            dictEngage[node[0]] = node[1]['CreatedAt']
    if (len(dictEngage) >0 ):
        sortedDictT = sorted(
            dictEngage.items(),
            key=lambda x: datetime.strptime(x[1], '%a %b %d %H:%M:%S %Y'), reverse=False
        )

        sortedDictR = sorted(
            dictEngage.items(),
            key=lambda x: datetime.strptime(x[1], '%a %b %d %H:%M:%S %Y'), reverse=True
        )
        tw = next(iter(sortedDictT))
        rw = next(iter(sortedDictR))
        # print(tw)
        # print(rw)
        diff = datetime.strptime(rw[1], datetimeFormat) - datetime.strptime(tw[1], datetimeFormat)
        hours = (diff.days) * 24 + (diff.seconds) / 3600
        return hours

def meanPuser(G):
    counter = 1
    total=0
    for node in G.nodes(data=True):
        if (node[1]['id'] == 3):
                counter+=1
                total += node[1]['user'][3]
    return total/counter

def sentiment_analyzer_scores(sentence):

    score = analyser.polarity_scores(sentence)
    return score

def crtStanceNet(G):
    Gp=nx.Graph()
    for node in G.nodes(data=True):
        if node[1]['id']==4:
            pid=node[0]
            sentence=node[1]['text']
            score=sentiment_analyzer_scores(sentence)
            s = score['compound']
            Gp.add_node(pid,score=s)
    n_list = list(Gp.nodes(data=True))
    for i in range(len(n_list)):
        sen1 = n_list[i][1]['score']
        for j in range(len(n_list)):
            sen2 = n_list[j][1]['score']
            if i != j and nodes_connected(Gp,n_list[i][0],n_list[j][0]) == False and abs(sen1 - sen2) < .5:
                Gp.add_edge(n_list[i][0], n_list[j][0], weight = 1 / (abs(sen1 - sen2) + .01))
    return Gp

def nodes_connected(Gp,u, v):
    return u in Gp.neighbors(v)

def TotalSen(Gp):
    score=0
    for node in Gp.nodes(data=True):
        score+=node[1]['score']
    return score

def DicSen(Gp):
    dic={}
    for node in Gp.nodes(data=True):
       dic[node[0]]=node[1]['score']
    return dic

def key_func(x):
    return x[-9:]
for news in sorted(os.listdir(Path),key=lambda x: int(x.split('.')[0][0:3])):

    print(news)
    data=[]
    G = nx.read_gpickle(join(Path,news))
    #emptyTw = findTws(G)
    #list.append(emptyTw)
    total=totalNode(G)
    data.append(total)
    totalTweet=findTtw(G)
    data.append(totalTweet)
    totalRetweet=findTrw(G)
    data.append(totalRetweet)
    totalReply=findTrp(G)
    data.append(totalReply)
    #dict=NumOutDegree(G)
    #maxOutDeg=MaxOutDegree(dict)
    #list.append(maxOutDeg)
    height=totalHeight(G)
    data.append(height)
    H=calFrequency(G)
    frequency=H/total
    frequency=round(frequency,2)
    data.append(frequency)
    vrfUsr=NumVrfRe(G)
    data.append(vrfUsr)
    dict=NumStsRe(G)
    numofNormal=dict['normal']
    numofLeader=dict['leader']
    data.append(numofNormal)
    data.append(numofLeader)
    Gp=crtStanceNet(G)
    totalSentiment=TotalSen(Gp)
    totalSentiment=round(totalSentiment,2)
    data.append(totalSentiment)
    # diameter=0
    # if(len(Gp.nodes())>0):
    #    diameter=nx.diameter(Gp)
    # data.append(diameter)
    dicSen=DicSen(Gp)
    cent=0
    if(len(Gp)>0):
        centDic=nx.betweenness_centrality(Gp)
        pid=next(iter(centDic))
        cent=dicSen[pid]
        cent=round(cent,2)
    data.append(cent)
    #arr=np.array(data)
    #print(data)
    with open("temp_real.csv", "a",newline='') as fp:
        wr = csv.writer(fp)
        wr.writerow(data)
