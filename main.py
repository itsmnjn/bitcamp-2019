import nltk
from nltk.wsd import lesk

import support.scrape as scrape

from pywsd.similarity import max_similarity,similarity_by_path
from pywsd.lesk import simple_lesk, adapted_lesk, cosine_lesk,original_lesk

from nltk.tokenize import PunktSentenceTokenizer,sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet as wn
import string
import operator


from frenetic.frenetic import *

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np

# Languages
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer


#targetLang = "english"
targetLang = "french"


fwn = None
if targetLang == "french":
    fwn = FreNetic("./frenetic/data/wolf.xml") 


stop_words = set(stopwords.words(targetLang)) 

def simpleFilter(sentence):
    filtered_sent = []
    
    lemmatizer = None
    if targetLang == "french":
        lemmatizer = FrenchLefffLemmatizer()
    else:
        lemmatizer = WordNetLemmatizer()
    
    
    stop_words = set(stopwords.words(targetLang))
    words = word_tokenize(sentence)

    for w in words:
        if w not in stop_words:
            filtered_sent.append(lemmatizer.lemmatize(w))

    return filtered_sent

def listToString(inputSentList):
    return ' '.join(inputSentList)

def viewAllDefinitions(wordStr):
    resList = []
    for syn in wn.synsets(wordStr):
        resList.append(syn.definition())
    return resList

def topRelevSent(targetWord):
    return

def simpleFilter(sentence):
    filtered_sent = []
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words(targetLang))
    words = word_tokenize(sentence)

    for w in words:
        if w not in stop_words:
            filtered_sent.append(lemmatizer.lemmatize(w))
    return listToString(filtered_sent)

def simpleFilterList(sentList):
    resList = []
    for sent in sentList:
        sent = sent.translate(str.maketrans('', '', string.punctuation))
        resList.append(simpleFilter(sent))
    return resList

def combineWordVec(a,b,aVec,bVec):
    aDf = pd.DataFrame(a.toarray(),columns=aVec.get_feature_names())
    bDf = pd.DataFrame(b.toarray(),columns=bVec.get_feature_names())

    combinedDf = pd.concat([aDf, bDf],sort=False).fillna(value=0.0)
    aRes = combinedDf.iloc[0].values
    bRes = combinedDf.iloc[1].values
    return aRes,bRes
    
def calcCosSim(a,b):
    # Calculate cosine simularity
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
    
def leskAlgoFr(sentence,ambiguous):
    synsets = fwn.synsets("cœur")
    
    sentence = simpleFilter(sentence)
    
    resAr = []
    for test in synsets:
        # We calculate cosine simularity
        vecSent = CountVectorizer()
        sentenceFreq = vecSent.fit_transform([sentence])
        
        definition = test.defn()
        
        vecDef = CountVectorizer()
        definitionFreq = vecDef.fit_transform([definition])
        
        defRes,sentRes = combineWordVec(definitionFreq,sentenceFreq,vecDef,vecSent)
        
        res = calcCosSim(defRes,sentRes)
        resAr.append(res)
        
    return synsets[np.argmax(np.asarray(resAr))].defn()





def seperateByDef(targetWord):
    # Returns a dictionary sorted by defintion

    sentList = None
    if targetLang == "french":

        sentList = scrape.scrapeFR(targetWord)
    else:
        sentList = scrape.scrape(targetWord)

    dictDef = {}
    for i,sent in enumerate(sentList):
        defineSent = None
        if targetLang == "french":
            defineSent = leskAlgoFr(sent,targetWord)
        else:
            #defineSent = cosine_lesk(sent,targetWord).definition()
            defineSent = adapted_lesk(sent,targetWord).definition()

        if defineSent not in dictDef:
            dictDef[defineSent] = [sent]
        else:
            dictDef[defineSent].append(sent)
    return dictDef

def printDictKeysVals(inputDict):
    for key in inputDict.keys():
        print('-------------------------------------------------------')
        print('Def: ', key)
        for value in inputDict[key]:
            print('        ', value)

def getDef(sent,targetWord):
    # Get defintion of word

    if targetLang == "french":
        defineSent = leskAlgoFr(sent,targetWord)
    else:
        #defineSent = cosine_lesk(sent,targetWord).definition()
        #defineSent = adapted_lesk(sent,targetWord).definition()
        defineSent = original_lesk(sent,targetWord).definition()

    return defineSent

def printDefExampleSent(inputDict,wordDef):
    print('Definition: ')
    print(wordDef)
    print('\n\n\n')
    print('Example sentence:')



    if wordDef not in inputDict:
        print('No example sentences found')
        return

    for sent in inputDict[wordDef]:
        print('-',sent)
        print('')


def countDefFreq(inputDict,n):
    resDict = {}
    for key in inputDict.keys():
        resDict[key] = len(inputDict[key])
    return getTopDefEntries(resDict, n)

def getTopDefEntries(inputDict, n):
    return dict(sorted(inputDict.items(), key=operator.itemgetter(1), reverse=True)[:n])


targetWord = 'cœur'
#testSent = 'He does not have money in his bank account'
testSent = 'Sa carte était la huit de cœur'



dictDef = seperateByDef(targetWord)
wordDef = getDef(testSent,targetWord)

#printDefExampleSent(dictDef,wordDef)
#printDictKeysVals(dictDef)



# Print out frequency of each definiton used
topRes = countDefFreq(dictDef, 5)



print('\n\n\n')
print('--------------------------------------------')
print('Input word: ', targetWord)
print('Input sentence: ', testSent)
print('\n\n\n')

print('--------------------------------------------')
print('\n\n\n')

dictDef = seperateByDef(targetWord)
wordDef = getDef(testSent,targetWord)

printDefExampleSent(dictDef,wordDef)
#printDictKeysVals(dictDef)

print('--------------------------------------------')
print('Most frequently used context')
print('\n\n\n')
# Print out frequency of each definiton used  (This is the print out the most frequently used context part)
topRes = countDefFreq(dictDef, 5)

# Top used context
for key in topRes.keys():
    print(key,': ', topRes[key])

print('\n\n\n')
print('Sentences of the most frequently used context')
# These are the sentences of the top used context printed out

for key in topRes.keys():
    print('Context: ', key)
    for sent in dictDef[key][:5]:
        print('    - ', sent)
    print('\n\n')
