import os
import re
from stop_words import get_stop_words
from math import log

allClasses = ['comp.graphics',
            'comp.os.ms-windows.misc',
            'comp.sys.ibm.pc.hardware',
            'comp.sys.mac.hardware',
            'comp.windows.x',
            'rec.autos',
            'rec.motorcycles',
            'rec.sport.baseball',
            'rec.sport.hockey',
            'sci.crypt',
            'sci.electronics',
            'sci.med',
            'sci.space',
            'misc.forsale',    
            'talk.politics.misc',
            'talk.politics.guns',
            'talk.politics.mideast',
            'talk.religion.misc',
            'alt.atheism',
            'soc.religion.christian']

classesChosen = ['talk.politics.misc','talk.politics.guns','misc.forsale','comp.sys.mac.hardware','comp.windows.x']
stop_words = get_stop_words('english')
train_data = 'T:/Sem 1/CS 6375- Machine Learning/Naive Bayes/20news-bydate-train/'
test_data = 'T:/Sem 1/CS 6375- Machine Learning/Naive Bayes/20news-bydate-test/'
vocabulary = {'talk.politics.misc':{},'talk.politics.guns':{},'misc.forsale':{},'comp.sys.mac.hardware':{},
              'comp.windows.x':{}}
no_of_class_docs = {'talk.politics.misc':0,'talk.politics.guns':0,'misc.forsale':0,'comp.sys.mac.hardware':0,
              'comp.windows.x':0}
prior = {'talk.politics.misc':0,'talk.politics.guns':0,'misc.forsale':0,'comp.sys.mac.hardware':0,
              'comp.windows.x':0}
conditional_probs = {'talk.politics.misc':{},'talk.politics.guns':{},'misc.forsale':{},'comp.sys.mac.hardware':{},
              'comp.windows.x':{}}

total_terms_in_class = {'talk.politics.misc':0,'talk.politics.guns':0,'misc.forsale':0,'comp.sys.mac.hardware':0,
              'comp.windows.x':0}
no_of_docs = 0

for train_data, dirs, files in os.walk(train_data):
    for classFolder in dirs:
        if classFolder in classesChosen:
            for subFolder, subDirs, docs in os.walk(train_data+classFolder+'/'):
                for eachDoc in docs:
                    no_of_docs = no_of_docs + 1 
                    no_of_class_docs.update({classFolder: no_of_class_docs.get(classFolder)+1})
                    docPath = train_data+classFolder+'/'+eachDoc
                    readFlag = False
                    with open(docPath,'r') as f:
                        for line in f:
                            words = filter(None,re.split(r'\W|\d', line))
                            if not readFlag:
                                if 'Lines' in words:
                                    readFlag = True
                            else:
                                for eachWord in words:
                                    #Checking for stop words
                                    if eachWord not in stop_words:
                                        if vocabulary[classFolder].get(eachWord) is None:
                                            vocabulary[classFolder][eachWord] = 1
                                        else:
                                            vocabulary[classFolder][eachWord] = vocabulary[classFolder][eachWord] + 1
                                        
total_terms_in_vocabulary = 0
for eachClass in vocabulary:
    total_terms_in_vocabulary = total_terms_in_vocabulary + len(vocabulary.get(eachClass))
    
for eachClass in vocabulary:
    words = vocabulary.get(eachClass)
    prior[eachClass] = float(no_of_class_docs[eachClass])/no_of_docs
    print "(",eachClass,":",prior[eachClass],")"
    for eachWord in words:
        total_terms_in_class[eachClass] = total_terms_in_class[eachClass] + words[eachWord]
    for eachWord in words:
        count = words[eachWord]
        conditional_probs[eachClass][eachWord] = float(count + 1)/(total_terms_in_class[eachClass] + total_terms_in_vocabulary)
#         print eachClass,",",eachWord,":",conditional_probs[eachClass][eachWord]


def determineClass(docPath):
    bestClass = None
    maxScore = None
    for eachClass in vocabulary:
        score = 0
        # Initializing the best class as the first class
        if bestClass is None:
            bestClass = eachClass
        score = score + log(prior[eachClass])
        readFlag = False
        with open(docPath,'r') as f:
            for line in f:
                words = filter(None,re.split(r'\W|\d', line))
                if not readFlag:
                    if 'Lines' in words:
                        readFlag = True
                else:
                    for eachWord in words:
                        if eachWord not in stop_words:
                            cond_prob = conditional_probs.get(eachClass).get(eachWord)
                            #Checking if the word is not available in the vocabulary
                            if cond_prob is None:
                                cond_prob = float(1)/(total_terms_in_class[eachClass] + total_terms_in_vocabulary)
                            score = score + log(cond_prob)
#         print "class:",eachClass,",score:",score
        if maxScore is None:
            maxScore = score
        if score >= maxScore:
            maxScore = score
            bestClass = eachClass
    return bestClass
                    

# Test
correct_predictions = 0
total_test_docs = 0
for test_data, dirs, files in os.walk(test_data):
    for classFolder in dirs:
        if classFolder in classesChosen:
            for subFolder, subDirs, docs in os.walk(test_data+classFolder+'/'):
                for eachDoc in docs:
                    total_test_docs = total_test_docs + 1
                    docPath = test_data+classFolder+'/'+eachDoc
                    predicted_class = determineClass(docPath)
#                     print "Predicted class",predicted_class
#                     print "class:", classFolder
                    if predicted_class == classFolder:
                        correct_predictions = correct_predictions + 1

accuracy = float(correct_predictions)/total_test_docs
print "Accuracy:",(accuracy*100),"%"       