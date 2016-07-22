from xml.dom.minidom import parse, parseString
from os import listdir
from os.path import isfile, join
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
import csv
import traceback, sys
from bs4 import BeautifulSoup as soup

mypath = '/Volumes/Media/Documents/Git/MachineLearning/out/'
onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)))]
onlyfiles = onlyfiles[1:len(onlyfiles)]

tagDict = set()
tagList = list()
textList = list()

def parseDocs():
    tagSet = set()
    for doc in onlyfiles:
        path = join(mypath, doc)

        tags, text = parseDoc(join(mypath, doc))

        tagSet.update(tags) # Just to know all unique tags
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

# def parseDoc(file):
#     dom = parse(file)
#     titleNodes = dom.getElementsByTagName('title')
#     tagNodes = dom.getElementsByTagName('tag')
#     textNode = dom.getElementsByTagName('text')
#     title = (titleNodes[0].firstChild.nodeValue + ' ') * 3
#
#     tags = [node.firstChild.nodeValue for node in tagNodes]
#     text = textNode[0].firstChild.nodeValue + title
#
#     return (tags, text)

tagDict = parseDocs()

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(textList)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print (X_train_tfidf.shape)

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(tagList)

classer = OneVsRestClassifier(LinearSVC(random_state=0)).fit(X_train_tfidf[:5000, :], y[:5000, :])

def evalTrainer():
    correct = 0
    for i in range(5001, len(textList)):
        correct = correct + pred(i)
    print (correct)
    print(correct/(len(textList)-5001))

def pred(index):
    predicted = classer.predict(X_train_tfidf[index, :])
    tagsPred = list()
    for i in predicted.nonzero()[1]:
        tagsPred.append(mlb.classes_.item(i))

    if set(tagsPred) == set(tagList[index]):
        return 1
    else:
        return 0
print (tagDict)

evalTrainer()
