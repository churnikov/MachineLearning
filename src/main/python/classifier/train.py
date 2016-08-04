from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import (chi2, SelectKBest, VarianceThreshold,
                                       f_classif, f_regression)
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from datetime import date
from parseUtils import parseDocs
from os.path import join
from nltk.stem.snowball import SnowballStemmer
from sklearn.pipeline import Pipeline
import csv
import numpy as np
import pdb

out_path = ("/Volumes/Media/Documents/Git/MachineLearning/src"
            "/main/resources/classifierOuts/")

(tagDict, tagList, textList, namesList) = parseDocs()
print(len(tagDict))

trainNum = 3922
testNumStart = 3923
testNumFinish = len(textList)

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


prepoc = Pipeline([('count', CountVectorizer(ngram_range=(1, 2),
                                               max_df=0.8, min_df=0.01,
                                               tokenizer=tokenize)),
                   ('tfidf', TfidfTransformer())])

X_train = prepoc.fit_transform(textList)
# Creating multilaber tags by binarizing them
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(tagList)

clf = Pipeline([('chi2', SelectKBest(chi2, k=5000)),
                ('svm', LinearSVC(random_state=0,
                                  class_weight='balanced',
                                  C=2.0))])

classer = OneVsRestClassifier(clf, n_jobs=1).fit(X_train[:trainNum, :],
                                                y[:trainNum, :])


print(X_train.shape)


def evalTrainer():
    # scr = classer.score(X_train[testNumStart:, :], y[testNumStart:, :])
    correct = 0
    true_pos = 0
    false_pos = 0
    false_neg = 0
    for i in range(testNumStart, testNumFinish):
        t_crrct, t_tp, t_fp, t_fn = pred(i)
        correct = correct + t_crrct
        true_pos = true_pos + t_tp
        false_pos = false_pos + t_fp
        false_neg = false_neg + t_fn
    # макро точность
    total_test = testNumFinish - testNumStart
    macro_precision = correct / total_test
    # микро точность
    tot_pred = true_pos + false_pos
    micro_prec = true_pos / tot_pred
    # полнота
    num_rel_tags = true_pos + false_neg
    recall = true_pos / num_rel_tags

    # F1
    F1 = 2 * micro_prec * recall / (micro_prec + recall)

    print('macro_precision = {mp}'.format(mp=macro_precision))
    print('micro_precision = {micp}'.format(micp=micro_prec))
    print('recall = {rcl}'.format(rcl=recall))
    print('F1 = {f1}'.format(f1=F1))
    print('macro_correct = {mcr}'.format(mcr=correct))
    print('micro_correct = {micr}'.format(micr=true_pos))
    print('false_neg_tags = {micfn}'.format(micfn=false_neg))
    print('false_pos_tags = {micfp}'.format(micfp=false_pos))
    print('total_test_docs = {ttd}'.format(ttd=total_test))
    print('n_of_pred_tags = {nopt}'.format(nopt=tot_pred))
    print('n_of_relevant_tags = {nort}'.format(nort=num_rel_tags))

    with open(join(out_path, 'results.txt'), 'a') as out:
        out.write('-' * 60)
        out.write('\n {date}'.format(date=date.today()))

        out.write('\n' + 'macro_precision = {mp}'.format(mp=macro_precision))
        out.write('\n' + 'micro_precision = {micp}'.format(micp=micro_prec))
        out.write('\n' + 'recall = {rcl}'.format(rcl=recall))
        out.write('\n' + 'F1 = {f1}'.format(f1=F1))

        out.write('\n' + 'macro_correct = {correct}'.format(correct=correct))
        out.write(' out of test = {total}'.format(total=total_test))

        out.write('\n' + 'micro_correct/true_pos_tags = {micr}'.format(micr=true_pos))
        out.write('\n' + 'false_neg_tags = {micfn}'.format(micfn=false_neg))
        out.write('\n' + 'false_pos_tags = {micfp}'.format(micfp=false_pos))

        out.write('\n' + 'n_of_predicted_tags = {nopt}'.format(nopt=tot_pred))
        out.write('\n' + 'n_of_relevant_tags = {nort}'.format(nort=num_rel_tags))

        docsnum = X_train.shape[0]
        terms = X_train.shape[1]
        out.write(
            '\n' + 'number of docs = {docsnum}; number of terms = {terms}'.format(docsnum=docsnum, terms=terms) + '\n')
        out.write('-' * 60)


def pred(index):
    predicted = classer.predict(X_train[index, :])
    tags_pred = list()
    for i in predicted.nonzero()[1]:
        tags_pred.append(mlb.classes_.item(i))

    true_pos = 0
    false_pos = 0
    false_neg = 0

    set_pred = set(tags_pred)
    set_tag = set(tagList[index])

    with open(join(out_path, 'output.txt'), 'a') as out:
        out.write('-' * 60)
        out.write('\ntext: {name}\n'.format(name=namesList[index]))
        out.write('predicted: ')
        for tag in tags_pred:
            out.write('{tag}; '.format(tag=tag))
        out.write('\nactual tags: ')
        for tag in set_tag:
            out.write('{tag}; '.format(tag=tag))
        out.write('\n' + '-' * 60 + '\n')

    if set_pred == set_tag:
        true_pos = len(tags_pred)
        return 1, true_pos, false_pos, false_neg
    else:
        allTags = set_pred.union(set_tag)
        for tag in allTags:
            if (tag in set_tag) and (tag in set_pred):
                true_pos += 1
            elif (tag in set_tag) and (tag not in set_pred):
                false_neg += 1
            elif (tag not in set_tag) and (tag in set_pred):
                false_pos += 1
        return 0, true_pos, false_pos, false_neg


def get_docs_distrib():
    for i in range(0, len(textList)):
        for tag in tagList[i]:
            tagDict[tag] += 1
    with open(join(out_path, 'output.csv'), 'w') as out:
        writer = csv.DictWriter(out, tagDict.keys())
        writer.writeheader()
        writer.writerow(tagDict)


# getDocsDistrib()

evalTrainer()
