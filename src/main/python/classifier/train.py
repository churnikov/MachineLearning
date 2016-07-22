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

tagDict = parseDocs()

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(textList)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print (X_train_tfidf.shape)

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(tagList)

trainNum = 5000
testNum = 5001
classer = OneVsRestClassifier(LinearSVC(random_state=0)).fit(X_train_tfidf[:trainNum, :], y[:trainNum, :])

def evalTrainer():
    correct = 0
    for i in range(testNum, len(textList)):
        correct = correct + pred(i)
    perc = correct/(len(textList)-(testNum))
    with open('results.txt', 'a') as out:
        out.write('-'*60)
        out.write('\n {date}'.format(date = date.today()))
        out.write('\n' + 'correct = {correct}'.format(correct = correct))
        out.write(' out of test = {total}'.format(total = testNum))
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
    w = csv.writer(open('output.csv', 'w'))
    for key, val in tagDict.items():
        w.writerow([key, val])

# getDocsDistrib()

evalTrainer()
