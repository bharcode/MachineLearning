# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 20:55:38 2012

@author: cyb
"""

CORPUS = "E:/data/facebook/Data/"

def evaluate(output):
    test = open(CORPUS + "validation/test.csv", "r")
    result = open(CORPUS + "validation/" + output, "r")
    result.readline()
    
    ap_sum = 0
    nuser = 0
    while True:
        line1 = test.readline()
        line2 = result.readline()
        if not line1 or not line2: break
        link_nodes = line1.split(',')[1].split()
        rec_nodes = line2.split(',')[1].split()
        ap = 0
        hit = n = 0
        for node in rec_nodes:
            n += 1
            if node in link_nodes:
                hit += 1
                ap += float(hit) / n
        ap /= len(link_nodes)
        ap_sum += ap
        nuser += 1
    test.close()
    result.close()
    print "AP@10 of", output, "is", ap_sum / nuser