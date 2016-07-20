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
        path = join(mypath, doc)

        tags, text = parseDoc(join(mypath, doc))

        tagSet.union(tags) # Just to know all unique tags
        tagList.append(tags)
        textList.append(text)

def parseDoc(file):
    dom = parse(file)

    titleNodes = dom.getElementsByTagName('title')
    tagNodes = dom.getElementsByTagName('tag')
    textNode = dom.getElementsByTagName('text')

    title = (titleNodes[0].firstChild.nodeValue + ' ') * 3

    tags = [node.firstChild.nodeValue for node in tagNodes]
    text = textNode[0].firstChild.nodeValue + title

    return (tags, text)

parseDocs()

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(textList)

tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(tagList)

classer = OneVsRestClassifier(LinearSVC(random_state=0)).fit(X_train_tfidf[:3160, :], y[:3160, :])

# tags_test, text = parseDoc(join(mypath, '23608.txt'))
# X_test_counts = count_vect.fit_transform(text)
# X_test_tfidf = tfidf_transformer.fit_transform(X_test_counts)

predicted = classer.predict(X_train_tfidf[3161, :])
print (predicted.shape)
print (len(textList))
a = predicted.nonzero()
for i in a[1]:
    print(mlb.classes_.item(i))

print(tagList[3161])



# print(X_train_counts.shape)
# print(len(tagSet))
