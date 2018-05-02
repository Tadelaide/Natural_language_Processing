# The result of the test is in output.txt
# Written by Hardy (hhardy2@sheffield.ac.uk)

import re
import os
import random
from collections import defaultdict
from collections import Counter

NEG_FOLDER = './review_polarity/txt_sentoken/neg/'
POS_FOLDER = './review_polarity/txt_sentoken/pos/'

STOP_WORDS = [
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
    'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being',
    'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't",
    'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during',
    'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have',
    "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers',
    'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm",
    "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's",
    'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off',
    'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves',
    'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's",
    'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the',
    'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these',
    'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through',
    'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd",
    "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's",
    'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's",
    'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've",
    'your', 'yours', 'yourself', 'yourselves', 'one', 'even', 'just', 'like', 'much',
    'many', 'also', 'always']

# STOP_WORDS = STOP_WORDS_MOVIE + STOP_WORDS

random.seed(2)
R = random.random()


def train():
    dataset = readDataSet(True)
    # --
    W_pos_neg = (defaultdict(int), defaultdict(int))
    W_pos_neg_sum = (defaultdict(int), defaultdict(int))
    c = 0
    # Set range to (0,1) to remove multiple passes
    for n in range(0, 10):
        # --
        # Comment this line to remove dataset shuffling
        random.shuffle(dataset, lambda: R)
        for D in dataset:
            x, y = D
            y_hat = argmax(x, W_pos_neg)
            if y_hat != y:
                W_pos_neg, W_pos_neg_sum = update_weight(W_pos_neg, W_pos_neg_sum, x, y, y_hat)
            else:
                W_pos_neg_sum = add_to_sum(W_pos_neg, W_pos_neg_sum)
            c += 1
        print('Training iteration: ' + str(n))
    # Replace with return W_pos_neg to remove averaging
    return averaging_weight(W_pos_neg_sum, c)


def test(W_pos_neg):
    dataset = readDataSet(False)
    f = open('output.txt', 'w+')
    outputString = ''
    correct = 0
    index = 0
    for D in dataset:
        x, y = D
        y_hat = argmax(x, W_pos_neg)
        if y_hat == y:
            correct += 1
        #print(index)
        index+=1
    outputString += 'Accuracy: ' + str(correct / len(dataset) * 100) + '%\n'
    outputString += 'Top Feature for Negative Class:\n'
    top = sorted(W_pos_neg[0].keys(), key=(lambda key: W_pos_neg[0][key]))[::-1]
    for item in top[:11]:
        outputString += item + '\n'
    outputString += 'Top Feature for Positive Class:\n'
    top = sorted(W_pos_neg[1].keys(), key=(lambda key: W_pos_neg[1][key]))[::-1]
    for item in top[:11]:
        outputString += item + '\n'
    f.write(outputString)

def readDataSet(isTraining):
    if isTraining:
        patternStr = r'^cv0*(?:[0-7][0-9][0-9]).*$'
    else:
        patternStr = r'^cv0*(?:[8-9][0-9][0-9]).*$'
    negFiles = [f for f in os.listdir(NEG_FOLDER) if re.match(patternStr, f)]
    posFiles = [f for f in os.listdir(POS_FOLDER) if re.match(patternStr, f)]
    negDataset = [open(NEG_FOLDER + file).read() for file in negFiles]
    posDataset = [open(POS_FOLDER + file).read() for file in posFiles]
    negBagofWords = []
    for negData in negDataset:
        bagOfWords = re.findall(r"[\w']+", negData)
        bagOfWords = [word for word in bagOfWords if word not in STOP_WORDS]
        negBagofWords.append((Counter(bagOfWords), 0))
    posBagofWords = []
    for posData in posDataset:
        bagOfWords = re.findall(r"[\w']+", posData)
        bagOfWords = [word for word in bagOfWords if word not in STOP_WORDS]
        posBagofWords.append((Counter(bagOfWords), 1))
    dataset = posBagofWords + negBagofWords
    return dataset

def argmax(x, W_pos_neg):
    max_result = float('-inf')
    y_hat = -1
    for i in range(len(W_pos_neg)):
        result = 0
        for word, count in x.items():
            result += W_pos_neg[i][word] * count
        if result > max_result:
            max_result = result
            y_hat = i
    return y_hat

def update_weight(W_pos_neg, W_pos_neg_sum, x, y, y_hat):
    for key, value in x.items():
        W_pos_neg[y][key] = W_pos_neg[y][key] + value
        W_pos_neg[y_hat][key] = W_pos_neg[y_hat][key] - value
        W_pos_neg_sum[y][key] += W_pos_neg[y][key]
        W_pos_neg_sum[y_hat][key] += W_pos_neg[y_hat][key]
    return W_pos_neg, W_pos_neg_sum

def add_to_sum(W_pos_neg, W_pos_neg_sum):
    for i in range(len(W_pos_neg)):
        for key, value in W_pos_neg[i].items():
            W_pos_neg_sum[i][key] += value
    return W_pos_neg_sum

def averaging_weight(W_pos_neg_sum, c):
    for i in range(len(W_pos_neg_sum)):
        for key, value in W_pos_neg_sum[i].items():
            W_pos_neg_sum[i][key] = value / c
    return W_pos_neg_sum

W_pos_neg = train()
test(W_pos_neg)
