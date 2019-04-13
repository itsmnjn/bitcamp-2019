import nltk
from nltk.wsd import lesk
from pywsd.similarity import max_similarity,similarity_by_path
from pywsd.lesk import simple_lesk, adapted_lesk, cosine_lesk,original_lesk

from nltk.tokenize import PunktSentenceTokenizer,sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet as wn
import string

import support.scrape as scrape


stop_words = set(stopwords.words('english')) 

def simpleFilter(sentence):
    filtered_sent = []
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
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
    stop_words = set(stopwords.words("english"))
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


def seperateByDef(targetWord):
    # Returns a dictionary sorted by defintion
    sentList = scrape.scrape(targetWord)
    
    dictDef = {}
    for i,sent in enumerate(sentList):
        
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
    
    #defineSent = cosine_lesk(sent,targetWord).definition()
    defineSent = adapted_lesk(sent,targetWord).definition() 
    
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
        
        
def countDefFreq(inputDict):
    resDict = {}
    for key in inputDict.keys():
        resDict[key] = len(inputDict[key])
    return sorted(resDict.items(), key=lambda kv: kv[1])

targetWord = 'bank'
#testSent = 'He does not have money in his bank account'
testSent = 'He ran out of money to deposit into the bank'

print('\n\n\n')
print('--------------------------------------------')
print('Input word: ', targetWord)
print('Input sentence: ', testSent)
print('\n\n\n')

print('--------------------------------------------')

dictDef = seperateByDef(targetWord)
wordDef = getDef(testSent,targetWord)

printDefExampleSent(dictDef,wordDef)
#printDictKeysVals(dictDef)

# Print out frequency of each definiton used
#print(countDefFreq(dictDef))



