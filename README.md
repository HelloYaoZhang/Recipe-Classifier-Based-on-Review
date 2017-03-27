# Recipe-Classifier-Based-on-Review
## About this project 
Implemented web scraping technique to collect text comments toward recipes from a restaurant website and extracted keywords from it. Build 
classifiers to predicte whether a recipe review is positive or negative only based on text information.

## Details
* Step one: the website we want to extract data is www.allrecipe.com. First, we decide that we only download data from chicken part. We let program download 
link of all recipe.
* Step two: because all of the links have already been stored into text file, so depending on that, the page can be downloaded.
* Step three: we indicate three text files to store the data we collect. Because the rating is the target we want to make prediction, and it contain 1 to 5, five levels. For the
easier assignment, all data can be set 4 and 5 combine as positive part; 3 as mild part; 1 and 2 as negative part. Then we extract the data we need (comment and rating) and save them into three individual files.
* Step four: for the better accuracy, the part of mild review is deleted.
* Step five: for the high-efficacy consideration, only 20,000 positive and negative we need as training set, the rest of the data is testing data.
* Step eight: train and test the model, using Tf-Idf and k-NN. Show the accuracy as result.


