from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup as soup

mypath = '/Volumes/Media/Documents/Git/MachineLearning/out/'

stopTagList = list()
with open('stopTagList.txt', 'r') as stl:
    for line in stl:
        stopTagList.append(line.rstrip('\n'))

def parseDocs(tag = None, texts_used = None, discard_tags = True, mypath = mypath):
    tag_set = set()
    tag_list = []
    text_list = []
    names_list = []
    onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and f.endswith('.txt'))]

    if not texts_used:
        for doc in onlyfiles:
            path = join(mypath, doc)
            tags, text = parseDoc(path)
            if 'notag' not in tags:
                if  (discard_tags) & ('discardTags' not in checkTag(tags)):
                    names_list.append(doc)
                    tag_set.update(tags)
                    tag_list.append(tags)
                    text_list.append(text)
        tagDict = dict.fromkeys(tag_set, 0)
    else:
        for doc in onlyfiles:
            if doc not in texts_used:
                path = join(mypath, doc)
                tags, text = parseDoc(path)
                if tag in tags:
                    names_list.append(doc)
                    tag_set.update(tags)
                    tag_list.append(tags)
                    text_list.append(text)
        tagDict = dict.fromkeys(tag_set, 0)
    return tagDict, tag_list, text_list, names_list

def parseDoc(file):
    fl = open(file, 'r')
    dom = soup(fl, 'lxml')
    text_wo_title = dom.find('text').get_text()
    # title = dom.find('title').get_text() * 3
    title = dom.find('title').get_text()
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

def update_file(path, f, tags):
    path_to_f = join(path, f)
    with open(path_to_f, 'r') as fl:
        dom = soup(fl, 'lxml')
        t = dom.find('tags')
        t.clear()
        for tag in tags:
            ta = dom.new_tag('tag')
            t.append(ta)
            ta.string = tag
        with open(path + 'pred' + f, 'w') as fll:
            html = soup.prettify(dom)
            fll.write(html)
