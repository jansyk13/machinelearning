#!/usr/bin/env python
from numpy import *
import operator

import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def create_data_set():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX, data, labels, k):
    data_size = data.shape[0]
    diff_mat = tile(inX, (data_size,1)) - data
    sq_diff_mat = diff_mat**2
    sq_distance = sq_diff_mat.sum(axis=1)
    distances = sq_distance**0.5
    sorted_dist_indicies = distances.argsort()
    class_count = {}
    for i in range(k):
         vote_I_label = labels[sorted_dist_indicies[i]]
         class_count[vote_I_label] = class_count.get(vote_I_label, 0) + 1
    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]

def auto_norm(data):
    min_vals = data.min(0)
    max_vals = data.max(0)
    ranges = max_vals - min_vals
    norm_data = zeros(shape(data))
    m = data.shape[0]
    norm_data = data - tile(min_vals, (m,1))
    norm_data = norm_data/tile(ranges, (m,1))
    return norm_data, ranges, min_vals

def file_2_matrix(path):
    # should be replaced by generator
    fr = open(path)
    number_of_lines = len(fr.readlines())
    return_mat = zeros((number_of_lines, 3))
    class_label_vector = []
    fr = open(path)
    index = 0
    for line in fr.readlines():
         line = line.strip()
         list_from_line = line.split('\t')
         return_mat[index,:] =  list_from_line[0:3]
         class_label_vector.append(int(list_from_line[-1]))
         index += 1
    return return_mat, class_label_vector

def example_dating_site():
    data, labels = file_2_matrix('datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(data[:,1], data[:,2], 15.0*array(labels), 15.0*array(labels))
    plt.show()

def example_A_B():
    data, labels = create_data_set()
    result = classify0([0,0], data, labels, 3)
    print result

# example_A_B()

example_dating_site()
