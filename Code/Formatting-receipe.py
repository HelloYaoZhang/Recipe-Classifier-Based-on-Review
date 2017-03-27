"""
1    it tastes bad
5    it tastes good
"""
result = open('training-data-set.txt','w') # open a file for writing the data after formatting
NReview = open('NegativeReviewInfo.txt').read() # read in the file containing negative review
PReview = open('PositiveReviewInfo.txt').read() # read in the file containing positive review

"""clean data, get rid of the certain useless words"""
NReview = NReview.replace("rating: 1","").replace("rating: 2","").replace("Negative comment: ","").replace("'","")
PReview = PReview.replace("rating: 4","").replace("rating: 5","").replace("Positive comment: ","").replace("'","")

NReview = NReview.split('\n')
PReview = PReview.split('\n')
NReview = filter(None, NReview) # delete the blank line
PReview = filter(None, PReview) # delete the blank line
""" get 20000 of the positive reviews and 20000 of the negative reviews for the training data set """
Ncounter = 0
Pcounter = 0
for line in NReview:
    result.write('1' + '\t' + line + '\n')
    Ncounter += 1
    if(Ncounter >= 20000):
        break
    
for line in PReview:
    result.write('5' + '\t' + line + '\n')
    Pcounter += 1
    if(Pcounter >= 20000):
        break

result.close
print "done!"  

result = open('training-data-set.txt','r')
count = 0
for line in enumerate(result):
    count += 1
result.close
print 'Total lines:', count  
