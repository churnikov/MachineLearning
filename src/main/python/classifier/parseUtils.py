from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup as soup

mypath = '/Volumes/Media/Documents/Git/MachineLearning/out/'
onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and f.endswith('.txt'))]
# while '.DS_Store' in onlyfiles:
#     del onlyfiles[onlyfiles.index('.DS_Store')]

stopTagList = list()
with open('stopTagList.txt', 'r') as stl:
    for line in stl:
        stopTagList.append(line.rstrip('\n'))

def parseDocs():
    tagSet = set()
    tagList = list()
    textList = list()
    for doc in onlyfiles:
        path = join(mypath, doc)
        tags, text = parseDoc(path)
        if 'notag' not in tags:
            tags = checkTag(tags)
            if 'discardTags' not in tags:
                tagSet.update(tags)
                tagList.append(tags)
                textList.append(text)
    tagDict = dict.fromkeys(tagSet, 0)
    return (tagDict, tagList, textList)

def parseDoc(file):
    fl = open(file, 'r')
    dom = soup(fl, 'lxml')
    text_wo_title = dom.find('text').get_text()
    title = dom.find('title').get_text() * 3
    text = text_wo_title + title
    tags = [x.get_text() for x in dom.findAll('tag')]

    return (tags, text)

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
        tagSet.add('discardTags')
    return list(tagSet)
