from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from datetime import date
from parseUtils import parseDocs
from os.path import join
import csv
import numpy as np
from nltk.stem.snowball import SnowballStemmer
import pdb

out_path = '/Volumes/Media/Documents/Git/MachineLearning/src/main/resources/classifierOuts/'

(tagDict, tagList, textList) = parseDocs()
print(len(tagDict))

stemmer = SnowballStemmer('russian')
def stem_tokenize(tokens):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

tkzr = CountVectorizer().build_tokenizer()
def tokenize(text):
    tokens = tkzr(text)
    return stem_tokenize(tokens)


#Counting/tokenizing/preprocessing words
count_vect = CountVectorizer(max_df=0.8, min_df=0.01,
                             ngram_range=(1, 2))
                            #  tokenizer=tokenize)
X_train_counts = count_vect.fit_transform(textList)

#Tranforming into tfidf matrix
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print (X_train_tfidf.shape)

#Creating multilaber tags by binarizing them
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(tagList)

trainNum = 3922
testNumStart = 3923
testNumFinish = len(textList)

classer = OneVsRestClassifier(LinearSVC(random_state=0,
                                        class_weight='balanced',
                                        C=2.0),
                              n_jobs=2).fit(X_train_tfidf[:trainNum, :],
                                            y[:trainNum, :])

def evalTrainer():
    # scr = classer.score(X_train_tfidf[testNumStart:, :], y[testNumStart:, :])
    correct = 0
    truePos = 0
    falsePos = 0
    falseNeg = 0
    for i in range(testNumStart, testNumFinish):
        t_crrct, t_tp, t_fp, t_fn = pred(i)
        correct = correct + t_crrct
        truePos = truePos + t_tp
        falsePos = falsePos + t_fp
        falseNeg = falseNeg + t_fn
    #макро точность
    totalTest = testNumFinish-testNumStart
    macro_precision = correct/totalTest
    #микро точность
    tot_pred = truePos + falsePos
    micro_prec = truePos/tot_pred
    #полнота
    numRelTags = truePos + falseNeg
    recall = truePos/numRelTags

    #F1
    F1 = 2 * micro_prec * recall / (micro_prec + recall)
    print('macro_precision = {mp}'.format(mp = macro_precision))
    print('micro_precision = {micp}'.format(micp = micro_prec))
    print('recall = {rcl}'.format(rcl = recall))
    print('F1 = {f1}'.format(f1 = F1))
    print('macro_correct = {mcr}'.format(mcr = correct))
    print('micro_correct = {micr}'.format(micr = truePos))
    print('false_neg_tags = {micfn}'.format(micfn = falseNeg))
    print('false_pos_tags = {micfp}'.format(micfp = falsePos))
    print('total_test_docs = {ttd}'.format(ttd = totalTest))
    print('n_of_pred_tags = {nopt}'.format(nopt = tot_pred))
    print('n_of_relevant_tags = {nort}'.format(nort = numRelTags))

    with open(join(out_path, 'results.txt'), 'a') as out:
        out.write('-'*60)
        out.write('\n {date}'.format(date = date.today()))

        out.write('\n' + 'macro_precision = {mp}'.format(mp = macro_precision))
        out.write('\n' + 'micro_precision = {micp}'.format(micp = micro_prec))
        out.write('\n' + 'recall = {rcl}'.format(rcl = recall))
        out.write('\n' + 'F1 = {f1}'.format(f1 = F1))

        out.write('\n' + 'macro_correct = {correct}'.format(correct = correct))
        out.write(' out of test = {total}'.format(total = totalTest))

        out.write('\n' + 'micro_correct/true_pos_tags = {micr}'.format(micr = truePos))
        out.write('\n' + 'false_neg_tags = {micfn}'.format(micfn = falseNeg))
        out.write('\n' + 'false_pos_tags = {micfp}'.format(micfp = falsePos))

        out.write('\n' + 'n_of_predicted_tags = {nopt}'.format(nopt = tot_pred))
        out.write('\n' + 'n_of_relevant_tags = {nort}'.format(nort = numRelTags))

        docsnum = X_train_tfidf.shape[0]
        terms = X_train_tfidf.shape[1]
        out.write('\n' + 'number of docs = {docsnum}; number of terms = {terms}'.format(docsnum = docsnum, terms = terms) + '\n')
        out.write('-'*60)

def pred(index):
    predicted = classer.predict(X_train_tfidf[index, :])
    tagsPred = list()
    for i in predicted.nonzero()[1]:
        tagsPred.append(mlb.classes_.item(i))

    truePos = 0
    falsePos = 0
    falseNeg = 0

    setPred = set(tagsPred)
    setTag = set(tagList[index])

    if setPred == setTag:
        truePos = len(tagsPred)
        return (1, truePos, falsePos, falseNeg)
    else:
        allTags = setPred.union(setTag)
        for tag in allTags:
            if (tag in setTag) and (tag in setPred):
                truePos = truePos + 1
            elif (tag in setTag) and (tag not in setPred):
                falseNeg = falseNeg + 1
            elif (tag not in setTag) and (tag in setPred):
                falsePos = falsePos + 1
        return (0, truePos, falsePos, falseNeg)

def getDocsDistrib():
    for i in range(0, len(textList)):
        for tag in tagList[i]:
            tagDict[tag] = tagDict[tag] + 1
    with open(join(out_path, 'output.csv'), 'w') as out:
        fieldNames = ['tag' , 'ocurs']
        writer = csv.DictWriter(out, tagDict.keys())
        writer.writeheader()
        writer.writerow(tagDict)

# getDocsDistrib()

evalTrainer()
