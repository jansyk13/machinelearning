#!/usr/bin/env python

import operator
from math import log

# using ID3 alg to split data

def test_data_set():
    data = [[1,1,'yes'],
            [1,1,'yes'],
            [1,0,'no'],
            [0,1,'no'],
            [0,1,'no']]
    labels = ['no surfacing', 'flippers']
    return data, labels


def calc_shannon_ent(data):
#    print 'Method call \'calc_shannon_ent\' data=\'%s\'' % data
    ent = 0.0
    number_entries = len(data)
    label_counts = {}
    for row in data:
        label = row[-1]
        if label not in label_counts.keys():
            label_counts[label] = 0
        label_counts[label] += 1
    for key in label_counts:
        prob = float(label_counts[key])/number_entries
        ent -= prob + log(prob,2)
#    print 'Entropy %d' % ent
    return ent


def split_data(data, axis, value, depth):
    indent = ''.join(['\t' for i in range(depth)])
    print '%sMethod call \'split_data\' data=\'%s\' axis=\'%s\' value=\'%s\'' % (indent, data, axis, value)
    reduced_data = []
    for row in data:
        if (row[axis] == value):
# cut out axis splitted by
            reduced_part = row[:axis]
            reduced_part.extend(row[axis+1:])
            reduced_data.append(reduced_part)
    print '%sReduced data \'%s\'' % (indent, reduced_data)
    return reduced_data


def choose_feature_to_split_on(data, depth):
    number_features = len(data[0]) - 1
    base_ent = calc_shannon_ent(data)
    best_info_gain = 0.0
    best_feature = -1
    for i in range(number_features):
        values_list = [sample[i] for sample in data]
        values_set = set(values_list)
        ent = 0.0
        for val in values_set:
            sub_data = split_data(data, i, val, depth)
            prob = len(sub_data)/float(len(data))
            ent -= prob * calc_shannon_ent(sub_data)
        info_gain = base_ent - ent
        if (info_gain > best_info_gain):
            best_info_gain = info_gain
            best_feature = i
    return best_feature


def majority_count(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def create_tree(data, labels, depth = 0):
    indent = ''.join(['\t' for i in range(depth)])
    print '%sMethod call \'create_tree\' depth=%d data=\'%s\' labels=\'%s\'' % (indent, depth, data, labels)
    class_list = [row[-1] for row in data]
    if class_list.count(class_list[0]) == len(class_list):
        val = class_list[0]
        print '%sAll classes are equal value=\'%s\'' % (indent, val)
        return val
    if len(data[0]) == 1:
        val = majority_count(class_list)
        print '%sFeature size==1 value=\'%s\'' % (indent, val)
        return val
    best_feature = choose_feature_to_split_on(data, depth)
    best_feature_label = labels[best_feature]
    tree = {best_feature_label:{}}
    del(labels[best_feature])
    feature_vals = [row[best_feature] for row in data]
    set_feature_vals = set(feature_vals)
    print '%sPresplitting depth=%d part of tree=\'%s\'' % (indent, depth, tree)
    for val in set_feature_vals:
        sub_labels = labels[:]
        sub_data = split_data(data, best_feature, val, depth)
        print '%sSubdata data=\'%s\'' % (indent, sub_data)
        sub_tree = create_tree(sub_data, sub_labels, (depth+1))
        print '%sSubtree path=\'%s\' value=\'%s\'' % (indent, val, sub_tree)
        tree[best_feature_label][val] = sub_tree
    return tree


print '\nkTree example:\n'
data, labels = test_data_set()
tree = create_tree(data,labels)
print '\n\nTree %s' % tree
