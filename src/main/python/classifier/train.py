from xml.dom.minidom import parse, parseString
from os import listdir
from os.path import isfile, join
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from bs4 import BeautifulSoup as soup
import csv
from datetime import date
import numpy as np
import re
import time

mypath = '/Volumes/Media/Documents/Git/MachineLearning/out/'
onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)))]
while '.DS_Store' in onlyfiles:
    del onlyfiles[onlyfiles.index('.DS_Store')]

tagList = list()
textList = list()

stopTagList = list()
with open('stopTagList.txt', 'r') as stl:
    for line in stl:
        stopTagList.append(line.rstrip('\n'))

def checkTag(tags): #This is pourly written method
    tagSet = set(tags)
    tagSetDiff = set()
    add = False
    for tag in tagSet:
        for category in stopTagList:
            if tag == category:
                add = True
                tagSetDiff.add(tag)

    if add:
        tagSet.difference_update(tagSetDiff)
        tagSet.add('Культура и туризм')
        if(len(tagSet) > 1):
            print (tagSet)
    return list(tagSet)

def parseDocs():
    tagSet = set()
    for doc in onlyfiles:
        path = join(mypath, doc)

        tags, text = parseDoc(join(mypath, doc))
        if 'notag' not in tags:
            tags = checkTag(tags)
            # if 'Культура и туризм' in tags:
            tagSet.update(tags)
            tagList.append(tags)
            textList.append(text)
    return dict.fromkeys(tagSet, 0)

def parseDoc(file):
    fl = open(file, 'r')
    dom = soup(fl, 'lxml')
    text_wo_title = dom.find('text').get_text()
    title = dom.find('title').get_text() * 3
    text = text_wo_title + title
    tags = [x.get_text() for x in dom.findAll('tag')]

    return (tags, text)
tagDict = parseDocs()
print(len(tagDict))

reg = "(?u)\b[\D(^-_\. )]+\b"
count_vect = CountVectorizer(max_df=0.8, min_df=0.01, ngram_range=(1, 2))
X_train_counts = count_vect.fit_transform(textList)

# count_terms = np.sum(X_train_counts.toarray(), axis=0)
# terms = count_vect.vocabulary_
# w = csv.writer(open('vocabulary_binary.csv', 'w'))
# w.writerow(['term', 'count'])
# for key, val in terms.items():
#     row = [key, count_terms[val]]
#     w.writerow(row)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print (X_train_tfidf.shape)

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(tagList)

trainNum = 5753
testNumStart = 5754
testNumFinish = len(textList)
classer = OneVsRestClassifier(LinearSVC(random_state=0, class_weight='balanced', C=2.0), n_jobs=2).fit(X_train_tfidf[:trainNum, :], y[:trainNum, :])

def evalTrainer():
    correct = 0
    for i in range(testNumStart, testNumFinish):
        correct = correct + pred(i)
    perc = correct/(testNumFinish-testNumStart)
    print(correct)
    print(perc)
    with open('results.txt', 'a') as out:
        out.write('-'*60)
        out.write('\n {date}'.format(date = date.today()))
        out.write('\n' + 'correct = {correct}'.format(correct = correct))
        out.write(' out of test = {total}'.format(total = len(textList)-testNumStart))
        out.write('\n' + 'percentage = {perc}'.format(perc=perc))
        docsnum = X_train_tfidf.shape[0]
        terms = X_train_tfidf.shape[1]
        out.write('\n' + 'number of docs = {docsnum}; number of terms = {terms}'.format(docsnum = docsnum, terms = terms) + '\n')
        out.write('-'*60)

def pred(index):
    predicted = classer.predict(X_train_tfidf[index, :])
    tagsPred = list()
    for i in predicted.nonzero()[1]:
        tagsPred.append(mlb.classes_.item(i))

    if set(tagsPred) == set(tagList[index]):
        return 1
    else:
        return 0

def getDocsDistrib():
    for i in range(0, len(textList)):
        for tag in tagList[i]:
            tagDict[tag] = tagDict[tag] + 1
    with open('output.csv', 'w') as out:
        fieldNames = ['tag' , 'ocurs']
        writer = csv.DictWriter(out, tagDict.keys())
        writer.writeheader()
        writer.writerow(tagDict)



# getDocsDistrib()

evalTrainer()
