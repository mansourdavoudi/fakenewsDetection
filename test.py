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
from networkx.utils import open_file
try:
    import cPickle as pickle
except ImportError:
    import pickle


Path_Fake="C:\dataset\\test"

def ComputeFtlr(G):

    print('calculation start !!!')
    hours=0
    datetimeFormat = "%a %b %d %H:%M:%S %Y"
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
        print(sortedDictT)
        print((sortedDictR))
        tw = next(iter(sortedDictT))
        rw = next(iter(sortedDictR))
        diff = datetime.strptime(rw[1], datetimeFormat) - datetime.strptime(tw[1], datetimeFormat)
        hours = (diff.days) * 24 + (diff.seconds) / 3600
        print("calculation done !!!")

    return hours

def calTime(tid):
    ctime=""
    with open ('retweets.json') as ReFile:
        rdata=json.load(ReFile)
        if(len(rdata[tid])>0):
            ctime=rdata[tid][0]['retweeted_status']['created_at']
    return ctime

def UsrInfo(data):

    flag="normal"
    followers=data['followers_count']
    friends=data['friends_count']
    if(friends>0):
        result = followers / friends
        if (result > 1):
            flag = "leader"
    return flag

def PEngage(id,data,G):

    if ('tweet_replies' in data):
        for i in range(len(data['tweet_replies'])):
            temp=data['tweet_replies'][i]
            pid = temp['id']
            utc = int(temp['created_at'])
            p_time = time.asctime(time.localtime(utc))
            G.add_node(str(pid),id=4,CreatedAt=p_time)
            G.add_edge(str(id), str(pid))
            if('engagement' in temp ):
                PEngage(pid,temp['engagement'],G)

def REngage(id,data,G):

    if('tweet_retweets' in data):

        for i in range(len(data['tweet_retweets'])):
            rid=data['tweet_retweets'][i]['id']
            verified = data['tweet_retweets'][i]['user']['verified']
            userType = UsrInfo(data['tweet_retweets'][i]['user'])
            r_time = data['tweet_retweets'][i]['created_at']
            li = r_time.split(" ")
            li.remove(li[4])
            r_time = ' '.join(li)
            G.add_node(str(rid), id=3, user=verified, usrType=userType, CreatedAt=r_time)
            G.add_edge(str(id), str(rid))
        for i in range(len(data['tweet_replies'])):
            temp = data['tweet_replies'][i]
            pid = temp['id']
            if ('engagement' in temp):
                REngage(pid,temp['engagement'],G)

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


dictNumEngage={}
dictNumTweet={}
dictNumRetweet={}
dictNumReply={}
dictNumEmptyTw={}
dictMaxHeight={}
dictTwMaxOutDegree={}
dictNumNotVrfRe={}
dictNumNormRe={}
dictNumNormReMaxOut={}
dictNumLeadReMaxOut={}
dictNumLedRe={}
dictTwMaxOutEngage={}
Trees_Fake=[]
news_sources={}
dictTFirstTlastR={}

news_sources = dict.fromkeys(news_sources, 0)

for news in os.listdir(Path_Fake):
    print("news --->" , news,"\n")
    G = nx.DiGraph()
    root=str(news)
    G.add_node(root,id=1)
    path=Path_Fake+"\\"+news
    os.chdir(path)
    with open ('news_article.json') as News:
        ndata=json.load(News)
        # if 'source' in ndata:
        #     source = ndata['source']
        #     if source in news_sources.keys():
        #         news_sources[source] += 1
        #     else:
        #         news_sources[source] = 1

    with open ('tweets.json') as TwFile:
        data=json.load(TwFile)
        ids=[]
        for i in range(len(data['tweets'])):
            id = data['tweets'][i]['tweet_id']
            ids.append(id)
            t_time = calTime(str(ids[i]))
            if(t_time!=""):
                li = t_time.split(" ")
                li.remove(li[4])
                t_time = ' '.join(li)
            if (t_time == ""):
                utc= data['tweets'][i]['created_at']
                t_time = time.asctime(time.localtime(utc))
            G.add_node(str(ids[i]), id=2,CreatedAt=t_time)
            G.add_edge(root, str(ids[i]))
    with open ('retweets.json') as ReFile:
        rdata=json.load(ReFile)
        for i in range(len(ids)):
            index=str(ids[i])
            if (rdata[index]!= None):
                for j in range(len(rdata[index])):
                    rid=rdata[index][j]['id']
                    userType=UsrInfo(rdata[index][j]['user'])
                    verified=rdata[index][j]['user']['verified']
                    r_time=rdata[index][j]['created_at']
                    li = r_time.split(" ")
                    li.remove(li[4])
                    r_time = ' '.join(li)
                    G.add_node(str(rid),id=3,user=verified,usrType=userType,CreatedAt=r_time)
                    G.add_edge(str(ids[i]),str(rid))

    with open ('replies.json',encoding="utf8") as PeFile:
        pdata=json.load(PeFile)
        for i in range(len(ids)):
            index = str(ids[i])
            if (len(pdata[index]) != 0 ):
                for j in range(len(pdata[index])):
                    temp=pdata[index][j]
                    pid=temp['id']
                    utc=int(temp['created_at'])
                    p_time = time.asctime(time.localtime(utc))
                    G.add_node(str(pid),id=4,CreatedAt=p_time)
                    G.add_edge(str(ids[i]),str(pid))
                    if ('engagement' in temp):
                           PEngage(pid,temp['engagement'],G)
                           REngage(pid,temp['engagement'],G)

    # for n in G.nodes(data=True):
    #
    #     if (n[0] == "687040837755219968"):
    #         Gtemp = dfs_tree(G, n[0])
    #         print(n[0], "--------------")
    # break

# for node in Gtemp.nodes(data=True):
#     print(node)
# plt.figure(1)
# nx.draw(Gtemp, with_labels=True, node_size=30)
# plt.show()

    # dictNumEngage[root]=[totalNode(G)]
    # dictNumTweet[root]=[findTtw(G)]
    # dictNumRetweet[root]=[findTrw(G)]
    # dictNumReply[root] = [findTrp(G)]
    # dictNumEmptyTw[root]=findTws(G)
    # dict=NumOutDegree(G)
    # maxOut=MaxOutDegree(dict)
    # dictTwMaxOutDegree[root]=maxOut
    # dictReMaxOutUserState=NumMaxOutStsRe(dict,maxOut,G)
    # dictNumNormReMaxOut[root]=dictReMaxOutUserState['normal']
    # dictNumLeadReMaxOut[root]=dictReMaxOutUserState['leader']
    # dictTwMaxOutEngage[root]=NumEngageTwMOut(dict,maxOut,G)
    # dictNumNotVrfRe[root]=NumNotVrfRe(G)
    # dictReUserState=NumStsRe(G)
    # dictNumNormRe[root]=dictReUserState['normal']
    # dictNumLedRe[root]=dictReUserState['leader']
    # dictMaxHeight[root]=totalHeight(G)
    dictTFirstTlastR[root]=ComputeFtlr(G)
    Trees_Fake.append(G)
    #break

nx.write_gpickle(G, "C:\\Users\\mansour\Desktop\\graph.gpickle")
#
# TotalNodeArr = np.array([val for val in dictNumEngage.values()])
# sumTotalNode=np.sum(TotalNodeArr)
# meanTotalNode=np.mean(TotalNodeArr)
# maxTotalNode=np.max(TotalNodeArr)
# minTotalNode=np.min(TotalNodeArr)
# stdTotalNode=np.std(TotalNodeArr)
# #
# #
# TotalTwArr = np.array([val for val in dictNumTweet.values()])
# sumTw=np.sum(TotalTwArr)
# meanTw=np.mean(TotalTwArr)
# maxTw=np.max(TotalTwArr)
# minTw=np.min(TotalTwArr)
# stdTw=np.std(TotalTwArr)
# #
# TotalReArr = np.array([val for val in dictNumRetweet.values()])
# sumRe=np.sum(TotalReArr)
# meanRe=np.mean(TotalReArr)
# maxRe=np.max(TotalReArr)
# minRe=np.min(TotalReArr)
# stdRe=np.std(TotalReArr)
# #
# #
# TotalRpArr = np.array([val for val in dictNumReply.values()])
# sumRp=np.sum(TotalRpArr)
# meanRp=np.mean(TotalRpArr)
# maxRp=np.max(TotalRpArr)
# minRp=np.min(TotalRpArr)
# stdRp=np.std(TotalRpArr)
# #
# #
# TwArr = np.array([val for val in dictNumEmptyTw.values()])
# sumEmptyTw = np.sum(TwArr)
# meanEmptyTw = np.mean(TwArr)
# maxEmptyTw=np.max(TwArr)
# minEmptyTw=np.min(TwArr)
# stdEmptyTw=np.std(TwArr)
# #
# #
# maxOutDegree=np.array([val for val in dictTwMaxOutDegree.values() if not math.isnan(val)])
# meanMaxOut=np.mean(maxOutDegree)
# maxMaxOut=np.max(maxOutDegree)
# minMaxOut=np.min(maxOutDegree)
# stdMaxOut=np.std(maxOutDegree)
# #
# maxOutEngage=np.array([val for val in dictTwMaxOutEngage.values()])
# sumMaxOutEngage=np.sum(maxOutEngage)
# meanMaxOutEngage=np.mean(maxOutEngage)
# maxMaxOutEngage=np.max(maxOutEngage)
# minMaxOutEngage=np.min(maxOutEngage)
# stdMaxOutEngage=np.std(maxOutEngage)
# #
# #
# reNotvrfArr=np.array([val for val in dictNumNotVrfRe.values()])
# sumVrf=np.sum(reNotvrfArr)
# meanVrf=np.mean(reNotvrfArr)
# maxVrf=np.max(reNotvrfArr)
# minVrf=np.min(reNotvrfArr)
# stdVrf=np.std(reNotvrfArr)
# #
# #
# NormalArr=np.array([val for val in dictNumNormRe.values()])
# sumNormal=np.sum(NormalArr)
# meanNormal=np.mean(NormalArr)
# maxNormal=np.max(NormalArr)
# minNormal=np.min(NormalArr)
# stdNormal=np.std(NormalArr)
# #
# NormalMaxArr=np.array([val for val in dictNumNormReMaxOut.values()])
# sumNormMax=np.sum(NormalMaxArr)
# meanNormMax=np.mean(NormalMaxArr)
# maxNormMax=np.max(NormalMaxArr)
# minNormMax=np.min(NormalMaxArr)
# stdNormMax=np.std(NormalMaxArr)
# #
# LeaderArr=np.array([val for val in dictNumLedRe.values()])
# sumLeader=np.sum(LeaderArr)
# meanLeader=np.mean(LeaderArr)
# maxLeader=np.max(LeaderArr)
# minLeader=np.min(LeaderArr)
# stdLeader=np.std(LeaderArr)
# #
# LeaderMaxArr=np.array([val for val in dictNumLeadReMaxOut.values()])
# sumLeadMax=np.sum(LeaderMaxArr)
# meanLeadMax=np.mean(LeaderMaxArr)
# maxLeadMax=np.max(LeaderMaxArr)
# minLeadMax=np.min(LeaderMaxArr)
# stdLeadMax=np.std(LeaderMaxArr)
# #
# print("\n")
# MaxHeight = np.array([val for val in dictMaxHeight.values()])
# meanMaxheight = np.mean(MaxHeight)
# maxMaxheight = np.max(MaxHeight)
# minMaxheight = np.min(MaxHeight)
# stdMaxheight = np.std(MaxHeight)
# #
TotalLifeCyc = np.array([val for val in dictTFirstTlastR.values()])
meanLC=np.mean(TotalLifeCyc)
maxLC=np.mean(TotalLifeCyc)
minLC=np.mean(TotalLifeCyc)
stdLC=np.mean(TotalLifeCyc)

f=open("C:\\Users\\mansour\Desktop\\politifact.txt","w+")

# f.write('Number of  nodes is %.3f \n' %(sumTotalNode) )
# f.write('mean of Num nodes is %.3f \n' %(meanTotalNode) )
# f.write('max of Num nodes is %.3f \n' %(maxTotalNode) )
# f.write('min of Num nodes is %.3f \n' %(minTotalNode) )
# f.write('std of Num nodes is %.3f \n' %(stdTotalNode) )
# f.write("\n")
#
# f.write('Number of tweets is %.3f \n' %(sumTw) )
# f.write('mean of Num tweets is %.3f \n' %(meanTw) )
# f.write('max of Num tweets is %.3f \n' %(maxTw) )
# f.write('min of Num tweets is %.3f \n' %(minTw) )
# f.write('std of Num tweets is %.3f \n' %(stdTw) )
# f.write("\n")
# f.write('Number of retweets is %.3f \n' %(sumRe) )
# f.write('mean of Num retweets is %.3f \n' %(meanRe) )
# f.write('max of Num retweets is %.3f \n' %(maxRe) )
# f.write('min of Num retweets is %.3f \n' %(minRe) )
# f.write('std of Num retweets is %.3f \n' %(stdRe) )
# f.write("\n")
# f.write('Number of replies is : %.3f \n' %(sumRp))
# f.write('mean of Num replies is : %.3f \n' %(meanRp))
# f.write('max of Num replies is : %.3f \n' %(maxRp))
# f.write('min of Num replies is : %.3f \n' %(minRp))
# f.write('std of Num replies is : %.3f \n' %(stdRp))
# f.write("\n")
# f.write('total number of tweets without engagements is : %.3f \n' %(sumEmptyTw))
# f.write('mean of Num tweets without engagements is : %.3f \n' %(meanEmptyTw))
# f.write('max of Num tweets without engagements is : %.3f \n' %(maxEmptyTw))
# f.write('min of Num tweets without engagements is : %.3f \n' %(minEmptyTw))
# f.write('std of Num tweets without engagements is : %.3f \n' %(stdEmptyTw))
# print("\n")
# f.write('mean of max Out Degree is : %.3f \n' %(meanMaxOut))
# f.write('max of max Out Degree is : %.3f \n' %(maxMaxOut))
# f.write('min of max Out Degree is : %.3f \n' %(minMaxOut))
# f.write('std of max Out Degree is : %.3f \n' %(stdMaxOut))
# print("\n")
# f.write('Total number of nodes in Cascades with most Out Degree is : %.3f \n' %(sumMaxOutEngage))
# f.write('mean nodes in Cascades with most Out Degree is : %.3f \n' %(meanMaxOutEngage))
# f.write('max nodes in Cascades with most Out Degree is : %.3f \n' %(maxMaxOutEngage))
# f.write('min nodes in Cascades with most Out Degree is : %.3f \n' %(minMaxOutEngage))
# f.write('std nodes in Cascades with most Out Degree is : %.3f \n' %(stdMaxOutEngage))
# print("\n")
# f.write('total number of retweets create by not verified users is : %.3f \n' %(sumVrf))
# f.write('mean of retweets create by not verified users is : %.3f \n' %(meanVrf))
# f.write('max of retweets create by not verified users is : %.3f \n' %(maxVrf))
# f.write('min of retweets create by not verified users is : %.3f \n' %(minVrf))
# f.write('std of retweets create by not verified users is : %.3f \n' %(stdVrf))
# print("\n")
# f.write('total number of retweets create by normal users is : %.3f \n' %(sumNormal))
# f.write('mean of retweets create by normal users is : %.3f \n' %(meanNormal))
# f.write('max of retweets create by normal users is : %.3f \n' %(maxNormal))
# f.write('min of retweets create by normal users is : %.3f \n' %(minNormal))
# f.write('std of retweets create by normal users is : %.3f \n' %(stdNormal))
# print("\n")
# f.write('total number of retweets create by normal users in cascades with most Out degree is : %.3f \n' %(sumNormMax))
# f.write('mean of retweets create by normal users in cascades with most Out degree is : %.3f \n' %(meanNormMax))
# f.write('max of retweets create by normal users in cascades with most Out degree is : %.3f \n' %(maxNormMax))
# f.write('min of retweets create by normal users in cascades with most Out degree is : %.3f \n' %(minNormMax))
# f.write('std of retweets create by normal users in cascades with most Out degree is : %.3f \n' %(stdNormMax))
#
# print("\n")
# f.write('total number of  retweets create by Leader users is : %.3f \n' %(sumLeader))
# f.write('mean of retweets create by Leader users is : %.3f \n' %(meanLeader))
# f.write('max of retweets create by Leader users is : %.3f \n' %(maxLeader))
# f.write('min of retweets create by Leader users is : %.3f \n' %(minLeader))
# f.write('std of retweets create by Leader users is : %.3f \n' %(stdLeader))
# print("\n")
# f.write('total number  of retweets create by leader users in cascades with most Out degree is : %.3f \n' %(sumLeadMax))
# f.write('mean  of retweets create by leader users in cascades with most Out degree is : %.3f \n' %(meanLeadMax))
# f.write('max of retweets create by leader users in cascades with most Out degree is : %.3f \n' %(maxLeadMax))
# f.write('min of retweets create by leader users in cascades with most Out degree is : %.3f \n' %(minLeadMax))
# f.write('std of retweets create by leader users in cascades with most Out degree is : %.3f \n' %(stdLeadMax))
# print("\n")
# f.write('mean of tree propagation height is : %.3f \n' %(meanMaxheight))
# f.write('max of tree propagation height is : %.3f \n' %(maxMaxheight))
# f.write('min of tree propagation height is : %.3f \n' %(minMaxheight))
# f.write('std of tree propagation height is : %.3f \n' %(stdMaxheight))
# print("\n")
f.write('mean of life cycle propagation of news is : %.3f \n' %(meanLC))
f.write('max of life cycle propagation of news is : %.3f \n' %(maxLC))
f.write('min of life cycle propagation of news is : %.3f \n' %(minLC))
f.write('std of life cycle propagation of news is : %.3f \n' %(stdLC))


f.close()



#
#
#     # counter+=1
#     # if counter==33:
#     #     break
# #print(nx.to_nested_tuple(G,root))
#
# # node_color = []
# #
# # for node in G.nodes(data=True):
# #     if node[1]['id'] == 1:
# #         node_color.append('yellow')
# #     # if the node has the attribute group1
# #     elif node[1]['id'] == 2:
# #         node_color.append('red')
# #     # if the node has the attribute group1
# #     elif node[1]['id'] == 3:
# #         node_color.append('green')
# #     # if the node has the attribute group1
# #     elif node[1]['id'] == 4:
# #         node_color.append('blue')
# #
# # # if the node has the attribute group1
# #
# # plt.figure(1)
# # nx.draw(G, with_labels=False, node_size=30, node_color=node_color)
# # plt.show()
#
# # totalTw=findTtw(G)
# # totalRw=findTrw(G)
# # totalRp=findTrp(G)
# # tws=findTws(G)
# # dict=NumOutDegree(G)
# # mean=MeanOutDegree(dict)
# #
# # height=totalHeight(G)
# # print(totalTw)
# # print(totalRw)
# # print(totalRp)
# # print(tws)
# # print(dict)
# # print(mean)
# # print(height)



