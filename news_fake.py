import os.path
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree
import json
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import OrderedDict
from operator import itemgetter
import csv
import time
from datetime import timedelta
from datetime import datetime


Path_Fake="C:\dataset\Politifact\\politifact_real_temp"

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

def PEngage(id,data,G,cl):

    if ('tweet_replies' in data):
        for i in range(len(data['tweet_replies'])):
            temp=data['tweet_replies'][i]
            pid = temp['id']
            txt=temp['text']
            utc = int(temp['created_at'])
            p_time = time.asctime(time.localtime(utc))
            diff = datetime.strptime(p_time, datetimeFormat) - datetime.strptime(baseTime, datetimeFormat)
            Hour = (diff.days) * 24 + (diff.seconds) / 3600
            if (Hour <= const*(cl + 1)):
                G.add_node(str(pid), id=4,text=txt, CreatedAt=p_time)
                G.add_edge(str(id), str(pid))
                if ('engagement' in temp):
                    PEngage(pid, temp['engagement'], G,cl)

def REngage(id,data,G,cl):

    if('tweet_retweets' in data):

        for i in range(len(data['tweet_retweets'])):
            rid=data['tweet_retweets'][i]['id']
            userList = UsrInfo(data['tweet_retweets'][i]['user'])
            r_time = data['tweet_retweets'][i]['created_at']
            li = r_time.split(" ")
            li.remove(li[4])
            r_time = ' '.join(li)
            diff = datetime.strptime(r_time, datetimeFormat) - datetime.strptime(baseTime, datetimeFormat)
            Hour = (diff.days) * 24 + (diff.seconds) / 3600
            if (Hour <= const*(cl + 1)):
                G.add_node(str(rid), id=3,user=userList,CreatedAt=r_time)
                G.add_edge(str(id), str(rid))
            for i in range(len(data['tweet_replies'])):
                temp = data['tweet_replies'][i]
                pid = temp['id']
                if ('engagement' in temp):
                    REngage(pid, temp['engagement'], G,cl)

def totalNode(G):
    counter = 0
    for node in G.nodes(data=True):
        if (node[1]['id'] != 1):
            counter += 1
    return counter

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
            li = list(G.successors(node[0]))
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

def NumNotVrfRe(G):
    counter=0
    for node in G.nodes(data=True):
        if(node[1]['id']==3):
            if(node[1]['user']==False):
                counter+=1
    return counter

def NumStsRe(G):
    dict={}
    dict['normal']=0
    dict['leader']=0
    for node in G.nodes(data=True):
        if(node[1]['id']==3):
            if(node[1]['usrType']=="normal"):
                dict['normal']+=1
            elif(node[1]['usrType']=="leader"):
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

counter=1
for news in os.listdir(Path_Fake):
    print("news --->" , news,"\n")
    root = str(news)
    path = Path_Fake + "\\" + news
    os.chdir(path)
    with open ('tweets.json') as TwFile:
        data=json.load(TwFile)
        ids=[]
        times={}
        for i in range(len(data['tweets'])):
            id = data['tweets'][i]['tweet_id']
            ids.append(id)
            t_time = calTime(str(ids[i]))
            if(t_time != ""):
                li = t_time.split(" ")
                li.remove(li[4])
                t_time = ' '.join(li)
            elif (t_time == ""):
                utc= data['tweets'][i]['created_at']
                t_time = time.asctime(time.localtime(utc))
            times[id]=t_time
        baseTime=calBaseTime(times)
    for cl in range(interval):
           G = nx.DiGraph()
           G.add_node(root, id=1)
           validTw=[]
           for tid in ids:
               diff = datetime.strptime(times[tid], datetimeFormat) - datetime.strptime(baseTime, datetimeFormat)
               Hour = (diff.days) * 24 + (diff.seconds) / 3600
               if Hour < const*(cl+1):
                  validTw.append(tid)
                  G.add_node(str(tid), id=2, CreatedAt=times[tid])
                  G.add_edge(root, str(tid))

           with open('retweets.json') as ReFile:
              rdata = json.load(ReFile)
              for i in range(len(validTw)):
                 index = str(validTw[i])
                 if (rdata[index] != None):
                    for j in range(len(rdata[index])):
                        rid = rdata[index][j]['id']
                        r_time = rdata[index][j]['created_at']
                        li = r_time.split(" ")
                        li.remove(li[4])
                        r_time = ' '.join(li)
                        userList = UsrInfo(rdata[index][j]['user'])
                        diff = datetime.strptime(r_time, datetimeFormat) - datetime.strptime(baseTime,datetimeFormat)
                        Hour = (diff.days) * 24 + (diff.seconds) / 3600
                        if Hour <= const*(cl+1):
                            G.add_node(str(rid), id=3,user=userList, CreatedAt=r_time)
                            G.add_edge(str(validTw[i]), str(rid))
           with open ('replies.json',encoding="utf8") as PeFile:
               pdata=json.load(PeFile)
               for i in range(len(validTw)):
                 index = str(validTw[i])
                 if (len(pdata[index]) != 0 ):
                    for j in range(len(pdata[index])):
                        temp=pdata[index][j]
                        pid=temp['id']
                        txt=temp['text']
                        utc=int(temp['created_at'])
                        p_time = time.asctime(time.localtime(utc))
                        diff = datetime.strptime(p_time, datetimeFormat) - datetime.strptime(baseTime, datetimeFormat)
                        Hour = (diff.days) * 24 + (diff.seconds) / 3600
                        if Hour <= const*(cl + 1):
                            G.add_node(str(pid), id=4,text=txt, CreatedAt=p_time)
                            G.add_edge(str(validTw[i]), str(pid))
                            if ('engagement' in temp):
                                PEngage(pid, temp['engagement'], G,cl)
                                REngage(pid, temp['engagement'], G,cl)
           if counter < 10:
               nx.write_gpickle(G, "C:\\Users\\mansour\Desktop\\temp2\\%s news %s.gpickle" % ("000"+str(counter),str(root)))
               counter+=1
           elif counter <100:
                nx.write_gpickle(G, "C:\\Users\\mansour\Desktop\\temp2\\%s news %s.gpickle" % ("00" + str(counter), str(root)))
                counter+=1
           elif(counter<1000):
               nx.write_gpickle(G,"C:\\Users\\mansour\Desktop\\temp2\\%s news %s.gpickle" % ("0" + str(counter), str(root)))
               counter+=1
           else:
               nx.write_gpickle(G,"C:\\Users\\mansour\Desktop\\temp2\\%s news %s.gpickle" % (str(counter), str(root)))
               counter+=1

















