import urllib2,re,os
"""
get link
"""
drop=0
"""
counter for the pages which has been lost during the try-except processing
"""
browser=urllib2.build_opener()
browser.addheaders=[('User-agent','Chrome/2.0')]

pagestoget=5
"""
total number of pages of chicken receipe
"""
filewriter=open('linkOfReview.txt','w')   

for page in range(1,pagestoget+1):
    print 'processing Receipe page: ',page,'\n'
    url='http://allrecipes.com/recipes/meat-and-poultry/chicken/main.aspx?soid=showcase_3&vm=l&evt19=1&p34=HR_ListView&Page='+str(page)+'#recipes'
    response=browser.open(url)
    myhtml=response.read()
    """
    get down to the pages of chicken-related receipes
    """
    segments=myhtml.split('ucListItem_lnkImage" href="http://allrecipes.com/recipe/') # separate each receipes
    for i in range(1,len(segments)):
        segmentpiece=segments[i]
        index=segmentpiece.find('/')
        name=segmentpiece[0:index]
        """
        get the name of the receipe which we will use to get the url of the review page
        """
        print name
        urlforPageNum='http://allrecipes.com/recipe/'+str(name)+'/detail.aspx?evt19=1'
        """
        get down to the detailed page of one certain receipe
        """
        try:        
            htmlforPageNum=(browser.open(urlforPageNum)).read()
            NumofReviewMatch=re.search('<span itemprop="reviewCount">(.*?)</span>',htmlforPageNum,re.S)
            if NumofReviewMatch:        
                NumofReview=NumofReviewMatch.group(1).strip()
                """
                get the review number of one certain receipe in order to get the number of review pages of that receipe
                """
                PageofReview=int(NumofReview)/10 + 1
                """
                divide the number of review pages by 10 and then plus 1 to get the total review page of that receipe
                """
                for ReviewPage in range(1,int(PageofReview)+1):
                    linkOfReview='http://allrecipes.com/recipe/'+str(name)+'/reviews.aspx?Page='+str(ReviewPage)
                    """
                    general form of different receipe review page
                    """
                    print 'processing Review page: ',ReviewPage
                    filewriter.write(linkOfReview+'\n')  
        except:
            drop=drop+PageofReview
            pass
filewriter.close()

"""
get page
"""
folder='Review'
if not os.path.exists(folder):
    os.mkdir(folder)
filereader=open('linkOfReview.txt')

for line in filereader:
    linkinfile=line.strip()
    webname=linkinfile[29:linkinfile.rfind('/')].strip()
    indexofPagenum=linkinfile.rfind('=')
    pageNum=linkinfile[indexofPagenum+1:]
    webname=webname+'Page'+pageNum
    print 'Downloading:',webname
    try:
        html=browser.open(linkinfile).read()
        filewriter=open(folder+'/'+webname,'w')
        filewriter.write(html)
        filewriter.close()
    except:
        drop=drop+1
        pass
    
filereader.close()

"""
get info
"""
files=os.listdir(folder)
filewriterP=open('PositiveReviewInfo.txt','w')
filewriterN=open('NegativeReviewInfo.txt','w')
filewriterM=open('MildReviewInfo.txt','w')

for review in files:
    name=None
    rating=None
    comment=None
    filereader=open(folder+'/'+review)
    text=filereader.read()
    filereader.close()
    """
    get rating & commment
    """
    segmain=text.split('<div class="rating-stars stars82x16 fl-none">')    
    """
    anchor for the comments and rating (10 for 1 review page)
    """
    for j in range(1,len(segmain)):
        segpiece=segmain[j]
        ratingMatch=re.search('<meta itemprop="ratingValue" content="(.*?)" />',segpiece,re.S)
        if ratingMatch:
            ratingMatchtext=ratingMatch.group(1).strip()
            ratingMatchtext=int(ratingMatchtext)
            if ratingMatchtext >= 4:
                rating=ratingMatchtext
                indexStart=segpiece.find('class="listItemReviewFull">')
                indexOver=segpiece.find('<div class="helpful">')
                comment=segpiece[indexStart+27:indexOver].strip()
                print 'Grabbing Data...'
                filewriterP.write('rating: '+str(rating)+'\n'+'Positive comment: '+str(comment)+'\n')
                print 'done!'
            elif ratingMatchtext <=2:
                rating=ratingMatchtext
                indexStart=segpiece.find('class="listItemReviewFull">')
                indexOver=segpiece.find('<div class="helpful">')
                comment=segpiece[indexStart+27:indexOver].strip()
                print 'Grabbing Data...'
                filewriterN.write('rating: '+str(rating)+'\n'+'Negative comment: '+str(comment)+'\n')
                print 'done!'
            else:
                rating=ratingMatchtext
                indexStart=segpiece.find('class="listItemReviewFull">')
                indexOver=segpiece.find('<div class="helpful">')
                comment=segpiece[indexStart+27:indexOver].strip()
                print 'Grabbing Data...'
                filewriterM.write('rating: '+str(rating)+'\n'+'Mild comment: '+str(comment)+'\n')
                print 'done!'
filewriterP.close()
filewriterN.close()    
filewriterM.close()
    
print drop,'pages have been dropped!!!'

            






























