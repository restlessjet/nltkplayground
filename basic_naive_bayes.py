import nltk
import random

trainreader = nltk.corpus.reader.CategorizedPlaintextCorpusReader('C:/Users/Sukanti/AppData/Roaming/nltk_data/corpora/sentiment_train/', r'.*\.txt', cat_pattern=r'(\w+)/*')

doctrain = [(list(trainreader.words(fileid)), category)
        for category in trainreader.categories()
        for fileid in trainreader.fileids(category)]
random.shuffle(doctrain)

print doctrain[10:]
