# from nltk.stem.snowball import SnowballStemmer
# from nltk import word_tokenize
# from sklearn.feature_extraction.text import CountVectorizer
#
# stemmer = SnowballStemmer('russian')
# string = 'правительственные органы Д.Медведев'
# cv = CountVectorizer()
# tokenize = cv.build_tokenizer()
# tokens = tokenize(string)
# for token in tokens:
#     print(stemmer.stem(token))

ls = [1, 1, 2, 3]
ls1 = [4, 5, 2]
lsSet = (set(ls))
lsSet1 = (set(ls1))
lsSetTot = lsSet.union(lsSet1)
print((lsSetTot))
for val in (lsSet):
    if 6 not in lsSetTot:
        print(val)
