from xml.dom.minidom import parse, parseString
from os import listdir
from os.path import isfile, join
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

mypath = '/Volumes/Media/Documents/Git/MachineLearning/out'
onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)))]
onlyfiles = onlyfiles[1:len(onlyfiles)]

tagSet = set()
tagList = list()
textList = list()

def parseDocs():
    for doc in onlyfiles:
        dom1 = parse(join(mypath, doc))

        titleNodes = dom1.getElementsByTagName('title')
        tagNodes = dom1.getElementsByTagName('tag')
        textNode = dom1.getElementsByTagName('text')

        title = titleNodes[0].firstChild.nodeValue
        title = (title + ' ') * 3

        tmpList = list()
        for node in tagNodes:
            tag = node.firstChild.nodeValue
            tagSet.add(tag)
            tmpList.append(tag)
        tagList.append(tmpList)

        text = textNode[0].firstChild.nodeValue
        textList.append(title + text)

parseDocs()

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(textList)

tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(tagList)

classer = OneVsRestClassifier(LinearSVC(random_state=0)).fit(X_train_tfidf, y)
predicted = classer.predict(X_train_tfidf[111])
a = predicted.nonzero()

for i in range(0, len(a)-1):
    print(mlb.classes_.item((a[1][i])))



# print(X_train_counts.shape)
# print(len(tagSet))
