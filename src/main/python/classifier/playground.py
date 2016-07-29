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

ls = ['a', 'b', 'c', 'd']
ls1 = [4, 5, 2]
with open('tst.txt', 'a') as out:
    for w in ls:
        out.write('wrd = {w}'.format(w = w))
