import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import csv
from datetime import date
import re
import time
from parseUtils import parseDocs

(tagDict, tagList, textList) = parseDocs()
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

trainNum = 3922
testNumStart = 3923
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
