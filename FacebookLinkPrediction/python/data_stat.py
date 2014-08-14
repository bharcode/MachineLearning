# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 22:22:15 2012

@author: cyb
"""

DIR = "E:/data/facebook/Data/"

import random

# 抽样validation
def sample_train_validation():
    train = open(DIR + "test/train.csv", "r")
    sample_train = open(DIR + "validation/train.csv", "w")
    sample_validation = open(DIR + "validation/test.csv", "w")
    lines = train.readlines()
    train.close()
    print len(lines)
    s = list(random.sample(xrange(len(lines)), len(lines) / 50))
    s.sort()
    j = 0
    pre_u = ''
    ulist = []
    for i in xrange(len(lines)):
        if j == len(s) or i != s[j]:
            print >> sample_train, lines[i],
        else:
            [u1, u2] = lines[i].split()
            if pre_u == '': pre_u = u1
            if u1 != pre_u:
                print >> sample_validation, pre_u + ',' + ' '.join(ulist)
                ulist = []
                pre_u = u1
            if len(ulist) == 10:
                print >> sample_train, lines[i],
            else: ulist.append(u2)
            j += 1
    print >> sample_validation, pre_u + ',' + ' '.join(ulist)
    sample_train.close()
    sample_validation.close()
    
# 抽样负例的时候可以用到
def user_followers_count():
    folds = ("test", "validation")
    for fold in folds:
        train = open(DIR + fold + "/train.csv", "r")
        out = open(DIR + fold + "/user_followers_count.txt", "w")
        counts = dict()
        for line in train:
            [u1, u2] = line.split()
            counts.setdefault(int(u2), 0)
            counts[int(u2)] += 1
        train.close()
        for u,c in counts.items():
            print >> out, u, c
        out.close()

# 统计用户的粉丝和关注者
def user_follow_relation():
    folds = ("test", "validation")
    for fold in folds:
        train = open(DIR + fold + "/train.csv", "r")
        followers = open(DIR + fold + "/followers.csv", "w")
        followees = open(DIR + fold + "/followees.csv", "w")   
        bi_follow = open(DIR + fold + "/bi_follow.csv", "w")
        unfolback_followees = open(DIR + fold + "/unfolback_followees.csv", "w")
        unfolback_followers = open(DIR + fold + "/unfolback_followers.csv", "w")
        u_flers = [[] for i in xrange(1862220+1)]
        u_flees = [[] for i in xrange(1862220+1)]
        for line in train:
            [u1, u2] = line.split()
            u_flers[int(u2)].append(int(u1))
            u_flees[int(u1)].append(int(u2))
        train.close()
        for u in xrange(1862220+1):
            if len(u_flers[u]) > 0:
                print >> followers, str(u) + "," + str(u_flers[u]).replace('[','').replace(']','').replace(',','')
            if len(u_flees[u]) > 0:
                print >> followees, str(u) + "," + str(u_flees[u]).replace('[','').replace(']','').replace(',','')
            list_1 = list(set(u_flers[u]) & set(u_flees[u]))
            list_2 = list(set(u_flers[u]) - set(u_flees[u]))
            list_3 = list(set(u_flees[u]) - set(u_flers[u]))
            if len(list_1) > 0:
                print >> bi_follow, str(u) + "," + str(list_1).replace('[','').replace(']','').replace(',','')
            if len(list_2) > 0:
                print >> unfolback_followers, str(u) + "," + str(list_2).replace('[','').replace(']','').replace(',','')
            if len(list_3) > 0:
                print >> unfolback_followees, str(u) + "," + str(list_3).replace('[','').replace(']','').replace(',','')
        followers.close()
        followees.close()
        bi_follow.close()
        unfolback_followers.close()
        unfolback_followees.close()
        
def friends_of_friends_v1():
    folds = ("test", "validation")
    for fold in folds:
        bi_follow = open(DIR + fold + "/bi_follow.csv", "r")
        followees = open(DIR + fold + "/followees.csv", "r")   
        unfol_friends_of_friends = open(DIR + fold + "/unfol_friends_of_friends.csv", "w")
        friends = [[] for i in xrange(1862220+1)]
        u_flees = [[] for i in xrange(1862220+1)]
        for line in bi_follow:
            [u, frs] = line.split(',')
            frs = frs.split()
            friends[int(u)] = frs
        bi_follow.close()
        for line in followees:
            [u, fs] = line.split(',')
            fs = fs.split()
            u_flees[int(u)] = fs
        followees.close()
        for u in xrange(1862220+1):
            uset = set()
            frs = friends[u]
            for f in frs:
                uset = uset | set(friends[int(f)])
            uset = uset - set(u_flees[u]) - set([str(u)])
            if len(uset) > 0:
                print >> unfol_friends_of_friends, str(u) + ',' + ' '.join(list(uset))
        unfol_friends_of_friends.close()

# v1 中产生的候选集太大
def friends_of_friends_v2():
    folds = ["test", "validation"]
    for fold in folds:
        bi_follow = open(DIR + fold + "/bi_follow.csv", "r")
        followees = open(DIR + fold + "/followees.csv", "r")   
        unfol_friends_of_friends = open(DIR + fold + "/unfol_friends_of_friends_v2.csv", "w")
        friends = [[] for i in xrange(1862220+1)]
        u_flees = [[] for i in xrange(1862220+1)]
        for line in bi_follow:
            [u, frs] = line.split(',')
            frs = frs.split()
            friends[int(u)] = frs
        bi_follow.close()
        for line in followees:
            [u, fs] = line.split(',')
            fs = fs.split()
            u_flees[int(u)] = fs
        followees.close()
        for u in xrange(1,1862220+1):
            udict = dict()
            frs = friends[u]
            for f in frs:
                for v in friends[int(f)]:
                    udict.setdefault(v, 0)
                    udict[v] += 1
            if str(u) in udict: udict.pop(str(u))
            for v in u_flees[u]: 
                if v in udict: udict.pop(v)
            ulist = sorted(udict.iteritems(), key=lambda (k,v):v, reverse=True)
            if len(ulist) > 0:
                line = ''
                for i in range(10):
                    if i == len(ulist): break
                    line += str(ulist[i][0]) + " "
                print >> unfol_friends_of_friends, str(u) + ',' + line.strip()
        unfol_friends_of_friends.close()
        
def candidates():
    folds = ["test", "validation"]
    for fold in folds:
        test = open(DIR + fold + "/test.csv", "r")
        test_u = set()
        for line in test:
            test_u.add(line.strip().split(',')[0])
        test.close()
        
        unfol_followers = open(DIR + fold + "/candidate_from_unfol_followers.csv", "r")
        unfol_friends_of_friends = open(DIR + fold + "/unfol_friends_of_friends_v2.csv", "r")
        candidate_f = open(DIR + fold + "/candidate.csv", "w")
        
        candidates = [[] for i in xrange(1862220+1)] 
        unfol_followers.readline()
        for line in unfol_followers:
            [u, fs] = line.split(',')
            fs = fs.split()
            for f in fs: candidates[int(u)].append(f)
        unfol_followers.close()    
        for line in unfol_friends_of_friends:
            [u, fs] = line.split(',')
            fs = fs.split()
            if len(candidates[int(u)]) > 0: continue
            for f in fs:
                candidates[int(u)].append(f)
        unfol_friends_of_friends.close()
        
        print >> candidate_f, "source_node,candidate_nodes"
        for u in xrange(1862220+1):
            if str(u) in test_u:
                print >> candidate_f, str(u) + "," + ' '.join(candidates[u])
        candidate_f.close()
    
    
    
    
    
    
    
    
    
    