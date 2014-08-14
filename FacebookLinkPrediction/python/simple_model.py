# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 22:49:47 2012

@author: cyb
"""

import csv

CORPUS = "E:/data/facebook/Data/"
    
def base_mode(DIR):
    r = open(CORPUS + DIR + 'train.csv','r')
    
    edges = set()
    for edge in r:
        [u1, u2] = edge.split()
        edges.add((u1, u2))
    
    missing_edges = set()
    for edge in edges:
        if (edge[1], edge[0]) not in edges:
            missing_edges.add((edge[1], edge[0]))
    
    missing_graph = dict()
    for edge in missing_edges:
        missing_graph.setdefault(edge[0], set()).add(edge[1])
    
    r = open(CORPUS + DIR + 'test.csv','r')
    
    test_list = list()
    for line in r:
        test_list.append(line.split(',')[0])
    
    test_lists = dict()
    for node in test_list:
        test_lists[node] = list(missing_graph.get(node, set()))
    
    submit = open(CORPUS + DIR + 'output.csv','wb')
    w = csv.writer(submit)
    w.writerow(['source_node','destination_nodes'])
    for node in test_list:
        w.writerow([node, " ".join(test_lists[node][0:10])])
    submit.close()
    
    candidate = open(CORPUS + DIR + 'candidate.csv','wb')
    w = csv.writer(candidate)
    w.writerow(['source_node','candidate_nodes'])
    for node in test_list:
        w.writerow([node, " ".join(test_lists[node])])
    candidate.close()
