'''
Created on Jun 25, 2017

@author: ruiwang
'''

from __future__ import division

import networkx as nx
import nltk



class GraphBuilder():

    def  __init__(self):
    
        self.doc_dict = {}
        self.windows_size = 2
 

    def build_unweight_graph(self, texts):

        graph = nx.Graph()

        for text in texts:

            for i in xrange(0, len(text)):
                for j in xrange(0, len(text)):
                    if i != j:
                        try:
                            graph.add_edge(text[i], text[j])
                        except Exception:
                            continue
                    j += 1
                i +=1                                    
        return graph
      

    def lDistance(self, firstString, secondString):
    
        if len(firstString) > len(secondString):
            firstString, secondString = secondString, firstString
        distances = range(len(firstString) + 1)
        for index2, char2 in enumerate(secondString):
            newDistances = [index2 + 1]
            for index1, char1 in enumerate(firstString):
                if char1 == char2:
                    newDistances.append(distances[index1])
                else:
                    newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
            distances = newDistances
        return distances[-1]           
