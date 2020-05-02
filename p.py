import os.path
from os import path
import networkx as nx
import scipy.spatial.distance as dist
from networkx.algorithms.traversal.depth_first_search import dfs_tree
import json
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import OrderedDict
from operator import itemgetter
import csv
from os.path import join
import time
from datetime import timedelta
from datetime import datetime
from node2vec import Node2Vec

Path="C:\dataset\Politifact\\politifact_fake_reply"

arr=np.zeros((181,65))

for count,news in enumerate(os.listdir(Path)):
    print("news --->" , news,"\n")
    G = nx.read_gpickle(join(Path,news))
    node2vec = Node2Vec(G, dimensions=64, walk_length=20, num_walks=10, p=2, q=1 / 2, weight_key='weight', workers=4)
    model = node2vec.fit(window=20, min_count=1, batch_words=4)
    temp = np.zeros((len(G.nodes()), 64))
    for cnt,node in enumerate(G.nodes(data=True)):
        vec = model.wv.get_vector(node[0])
        temp[cnt, :] = vec
    mat = temp.max(axis=0)
    mat = np.append(mat,0)
    arr[count, :] = mat
    print(mat)

np.savetxt("n2vf_reply.csv",arr,delimiter=",",fmt='%.2f')
