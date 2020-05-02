import os.path
import networkx as nx
import json
import matplotlib.pyplot as plt


def PEngage(id,data,G):
    if ('tweet_replies' in data):
        for i in range(len(data['tweet_replies'])):
            temp=data['tweet_replies'][i]
            pid = temp['id']
            G.add_node(str(pid),id=4)
            G.add_edge(str(id), str(pid))
            if('engagement' in temp ):
                PEngage(pid,temp['engagement'],G)

def REngage(id,data,G):

    if('tweet_retweets' in data):

        for i in range(len(data['tweet_retweets'])):
            rid=data['tweet_retweets'][i]['id']
            G.add_node(str(rid),id=3)
            G.add_edge(str(id), str(rid))
        for i in range(len(data['tweet_replies'])):
            temp = data['tweet_replies'][i]
            pid = temp['id']
            if ('engagement' in temp):
                REngage(pid,temp['engagement'],G)


Path_Real="C:\dataset\Politifact\politifact_real"
Path_Fake="C:\dataset\Politifact\politifact_fake"

Trees_Real=[]
Trees_Fake=[]

for news in os.listdir(Path_Real):
    print("news --->" , news,"\n")
    G = nx.DiGraph()
    root=str(news)
    G.add_node(root,id=1)
    path=Path_Real+"\\"+news
    os.chdir(path)

    with open ('tweets.json') as TwFile:
        data=json.load(TwFile)
        ids=[]
        for i in range(len(data['tweets'])):
            id = data['tweets'][i]['tweet_id']
            print(id,"\n")
            ids.append(id)
        for i in range(len(ids)):
            G.add_node(str(ids[i]),id=2)
            G.add_edge(root,str(ids[i]))

    with open ('retweets.json') as ReFile:
        rdata=json.load(ReFile)
        for i in range(len(ids)):
            index=str(ids[i])
            if (rdata[index]!= None):
                for j in range(len(rdata[index])):
                    rid=rdata[index][j]['id']
                    G.add_node(str(rid),id=3)
                    G.add_edge(str(ids[i]),str(rid))

    with open ('replies.json',encoding="utf8") as PeFile:
        pdata=json.load(PeFile)
        for i in range(len(ids)):
            index = str(ids[i])
            if (len(pdata[index]) != 0 ):
                for j in range(len(pdata[index])):
                    temp=pdata[index][j]
                    pid=temp['id']
                    G.add_node(str(pid),id=4)
                    G.add_edge(str(ids[i]),str(pid))
                    if ('engagement' in temp):
                           PEngage(pid,temp['engagement'],G)
                           REngage(pid,temp['engagement'],G)

    Trees_Real.append(G)

for news in os.listdir(Path_Fake):
    print("news --->" , news,"\n")
    G = nx.DiGraph()
    root=str(news)
    G.add_node(root,id=1)
    path=Path_Fake+"\\"+news
    os.chdir(path)

    with open ('tweets.json') as TwFile:
        data=json.load(TwFile)
        ids=[]
        for i in range(len(data['tweets'])):
            id = data['tweets'][i]['tweet_id']
            print(id,"\n")
            ids.append(id)
        for i in range(len(ids)):
            G.add_node(str(ids[i]),id=2)
            G.add_edge(root,str(ids[i]))

    with open ('retweets.json') as ReFile:
        rdata=json.load(ReFile)
        for i in range(len(ids)):
            index=str(ids[i])
            if (rdata[index]!= None):
                for j in range(len(rdata[index])):
                    rid=rdata[index][j]['id']
                    G.add_node(str(rid),id=3)
                    G.add_edge(str(ids[i]),str(rid))

    with open ('replies.json',encoding="utf8") as PeFile:
        pdata=json.load(PeFile)
        for i in range(len(ids)):
            index = str(ids[i])
            if (len(pdata[index]) != 0 ):
                for j in range(len(pdata[index])):
                    temp=pdata[index][j]
                    pid=temp['id']
                    G.add_node(str(pid),id=4)
                    G.add_edge(str(ids[i]),str(pid))
                    if ('engagement' in temp):
                           PEngage(pid,temp['engagement'],G)
                           REngage(pid,temp['engagement'],G)

    Trees_Fake.append(G)


#node_colors = []

# for i in range (len(Trees)):
#     tree=Trees[i]
#     node_color = []
#     for node in tree.nodes(data=True):
#         # if the node has the attribute group1
#         if node[1]['id'] == 1:
#             node_color.append('yellow')
#         # if the node has the attribute group1
#         elif node[1]['id'] == 2:
#             node_color.append('red')
#         # if the node has the attribute group1
#         elif node[1]['id'] == 3:
#             node_color.append('green')
#         # if the node has the attribute group1
#         elif node[1]['id'] == 4:
#             node_color.append('blue')
#     plt.figure(i)
#     nx.draw(tree, with_labels=False, node_size=30, node_color=node_color)
#     plt.show()

# draw graph with node attribute color
#plt.figure(1)
#nx.draw(G, node_size=50,node_color=gr, with_labels=False)

#for i in range(len(ids)):
    #print(nx.shortest_path_length(G, str(ids[i])),"\n")

