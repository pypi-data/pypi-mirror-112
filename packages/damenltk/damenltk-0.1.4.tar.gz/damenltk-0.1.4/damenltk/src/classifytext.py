from src.damenltk import DameNLTK
from nltk.corpus import PlaintextCorpusReader

dn = DameNLTK()

# corpus_root = '/usr/share/dict'

path_exploration = '../dataset/exploration/'
path_headhunters = '../dataset/headhunters/'
path_intelligence = '../dataset/intelligence/'
path_logistics = '../dataset/logistics/'
path_politics = '../dataset/politics/'
path_transportation = '../dataset/transportation/'
path_weapons = '../dataset/weapons/'

exploration = PlaintextCorpusReader(path_exploration, '.*')
headhunters = PlaintextCorpusReader(path_headhunters, '.*')
intelligence = PlaintextCorpusReader(path_intelligence, '.*')
logistics = PlaintextCorpusReader(path_logistics, '.*')
transportation = PlaintextCorpusReader(path_transportation, '.*')
weapons = PlaintextCorpusReader(path_weapons, '.*')

# print(exploration)
# print(exploration.fileids())

for fileid in exploration.fileids():
    num_chars = len(exploration.raw(fileid))
    words = exploration.words(fileid)
    print(words)
    num_words = len(words)
    print("printing number of words")
    print(num_words)
    print(words[0:3])
    if not string:
        string = "All work and no play makes jack dull boy. "
        string = string + "All work and no play makes jack a dull boy."
    stopWords = set(stopwords.words('english'))
    words = word_tokenize(string)
    wordsFiltered = []

    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)
    print(wordsFiltered)
    words2 = dn.remove_stopwords(words[0:3])
    print(words2)
