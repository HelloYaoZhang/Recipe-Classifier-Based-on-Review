from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from string import punctuation
import re,nltk
#nltk.download()

"""
read in the traning data
"""
text = open('training-data-set.txt','r+').read() 

"""
read in three libraries for negative words, positive words and 'not' words
"""
pLib = open('positive-words.txt').read()
pLines = pLib.split('\n')
nLib = open('negative-words.txt').read()
nLines = nLib.split('\n')
negaWord = set(['nothing', 'no', 'too', 'not', 'isnt', 'arent', 'dont', 'doesnt', 'wasnt', 'werent', 'didnt', 'havent', 'hasnt', 'wont', 'cant', 'couldnt', 'wouldnt', 'shouldnt'])

"""
open a new file for the traning data after preprocessing
"""
trainNew = open('trainNew.txt','w') 

"""
preprocessing data: clean the text and merge the 'not' word with the positive and negative words
"""
text = text.replace("'","")
reviews = text.split('\n')
reviews = filter(None, reviews) #remove blank lines

for review in reviews:   
    toks = review.strip().split('\t')   # split the tokens
    review = re.sub("[\W\d]", " ", toks[1].strip())  #delete all non-alpha in tok[1]
    reviewList = nltk.word_tokenize(review.lower()) 

    nWord = set(reviewList).intersection(set(nLines)) # find all the negative words
    pWord = set(reviewList).intersection(set(pLines)) # find all the positive words
    
    ncorr = 0
    pcorr = 0
    
    for word in pWord:
        index = reviewList.index(word) # find the location of positive words
        for i in range(1, 3): # search the two words ahead of the positive words 
            if(index - i < 0): # exception handle
                break
            if(reviewList[index - i] in negaWord): # if find 'not' word ahead, then merge them
                tempString_1 = reviewList[index]
                tempString = reviewList[index-i]+tempString_1
                reviewList.insert(index+1,tempString) # insert the combi-word into review
                reviewList.pop(index - i)
                reviewList.pop(index - 1)
                break 
    
    for word in nWord:
        index = reviewList.index(word) # find the location of negative words
        for i in range(1, 3): # search the two words ahead of the negative words
            if(index - i < 0): # exception handle
                break
            if(reviewList[index - i] in negaWord):
                tempString_1 = reviewList[index]
                tempString = reviewList[index-i]+tempString_1
                reviewList.insert(index+1,tempString) # insert the combi-word into review
                reviewList.pop(index - i)
                reviewList.pop(index - 1)
                break  
          
    reviewString = str(reviewList).replace("'","").replace(",","").replace("[","").replace("]","") # clean data
    trainNew.write(str(toks[0])+'\t'+reviewString+'\n') # write in the data to the txt after preprocessing

trainNew.close()

"""
Training Data input, Points and Labels extracted
"""
count = 0
points = []
labels = []
f=open('trainNew.txt')
for line in f:
#    print line
    toks = line.strip().split('\t')   # split the tokens
    if len(toks)>1:
        toks[1] = toks[1].replace(",", " ")
        for punct in list(punctuation):
            toks[1] = toks[1].replace(punct, "")
        points.append(toks[1])
        labels.append(toks[0])
    count += 1
#    print "processing line: ", count


f.close()  

''' test input port '''
text = open('self-test-data-set.txt','r+').read()
''' test input port '''

"""
preprocessing data: clean the text and merge the 'not' word with the positive and negative words
(do the same thing to the test data set as we do to the training set)
"""
pLib = open('positive-words.txt').read()
pLines = pLib.split('\n')
nLib = open('negative-words.txt').read()
nLines = nLib.split('\n')
negaWord = set(['nothing', 'no', 'too', 'not', 'isnt', 'arent', 'dont', 'doesnt', 'wasnt', 'werent', 'didnt', 'havent', 'hasnt', 'wont', 'cant', 'couldnt', 'wouldnt', 'shouldnt'])

testNew = open('testNew.txt','w') #store the reviews after shaping

text = text.replace("'","")
reviews = text.split('\n')
reviews = filter(None, reviews) #remove blank lines

for review in reviews:   
    toks = review.strip().split('\t')   # split the tokens
    review = re.sub("[\W\d]", " ", toks[1].strip())  #delete all non-alpha in tok[1]
    reviewList = nltk.word_tokenize(review.lower()) 

    nWord = set(reviewList).intersection(set(nLines))
    pWord = set(reviewList).intersection(set(pLines))
    
    ncorr = 0
    pcorr = 0
    
    for word in pWord:
        index = reviewList.index(word)
        for i in range(1, 3):
            if(index - i < 0):
                break
            if(reviewList[index - i] in negaWord):
                tempString_1 = reviewList[index]
                tempString = reviewList[index-i]+tempString_1
                reviewList.insert(index+1,tempString)
                reviewList.pop(index - i)
                reviewList.pop(index - 1)
                break 
    
    for word in nWord:
        index = reviewList.index(word)
        for i in range(1, 3):
            if(index - i < 0):
                break
            if(reviewList[index - i] in negaWord):
                tempString_1 = reviewList[index]
                tempString = reviewList[index-i]+tempString_1
                reviewList.insert(index+1,tempString) #insert the combi-word into review
                reviewList.pop(index - i)
                reviewList.pop(index - 1)
                break  
          
    reviewString = str(reviewList).replace("'","").replace(",","").replace("[","").replace("]","")
    testNew.write(str(toks[0])+'\t'+reviewString+'\n')

testNew.close()

"""
Testing Data input, Points and Labels extracted (Professor, please put your test data here~~~)
"""
f=open('testNew.txt')
tcount = 0
tpoints = []
tlabels = []
for line in f:
    toks = line.strip().split('\t')   # split the tokens  
    toks[1] = toks[1].replace(",", " ")   
    for punct in list(punctuation):
        toks[1] = toks[1].replace(punct, "")
    tpoints.append(toks[1])   
    tlabels.append(toks[0])
    tcount += 1
    print "processing line: ", tcount
f.close()     

"""
Train and test the model
"""   
# we will use this pipeline to tokenize both the training and testing data
pipe= Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf',  KNeighborsClassifier())])

#fit on the training data
print "Modeling...Please wait..."
model = pipe.fit(points, labels)    
print "Modeling Successful!!!"

#predict the labels of  the testing data
print "Predicting...Please wait..."
predicted=model.predict(tpoints)
print "Prediction Finished!!!"


#get the accuracy
print "Accuracy: ", np.mean(predicted == tlabels)
    

