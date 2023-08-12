import pandas as pd
import requests
# from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

scraped = "C:/Users/Win/OneDrive/Desktop/Test Assignment/Scraped"
stopwords = "C:/Users/Win/OneDrive/Desktop/Test Assignment/StopWords"
md = "C:/Users/Win/OneDrive/Desktop/Test Assignment/MasterDictionary"

ip = pd.read_excel('Input.xlsx')
ip.head()

sw = set()
for file in os.listdir(stopwords):
    with open(os.path.join(stopwords,file),'r') as f:
        sw.update(set(f.read().splitlines()))

#print(len(sw))

pw=set()
nw=set()
for file in os.listdir(md):
  if file =='positive-words.txt':
    with open(os.path.join(md,file),'r',encoding='ISO-8859-1') as f:
      pw.update(f.read().split())
  else:
    with open(os.path.join(md,file),'r',encoding='ISO-8859-1') as f:
      nw.update(f.read().split())

for i, row in ip.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    try:
        response = requests.get(url)
    except:
        print("Page Not found for URL_ID {}".format(url_id))

    try:
        soup = BeautifulSoup(response.content, 'html5lib')
    except:
        print("No Content for URL_ID {}".format(url_id))

    try:
        title = soup.find('h1').get_text()
    except:
        print("No title for URL_ID {}".format(url_id))
        continue

    content = ""
    try:
        for p in soup.find_all('p'):
            content += p.get_text()
    except:
        print("No Article for URL_ID {}".format(url_id))

    filename = scraped + '/' + str(url_id) + '.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(title + '\n' + content)


without_sw = []
c=0
for file in os.listdir(scraped):
  with open(os.path.join(scraped, file),'r', encoding='utf-8') as f:
    read = f.read()
#     res = re.findall(r'\w+', read)
    res = word_tokenize(read) 
    without_sw.append([word for word in res if word.lower() not in sw])



masterDict = {}
cpw = []
cnw =[]
pscore = []
nscore = []
polarity = []
subjectivityscore = []
for i in range(len(without_sw)):
    cpw.append([x for x in without_sw[i] if x.lower() in pw])
    pscore.append(len(cpw[i]))
    cnw.append([x for x in without_sw[i] if x.lower() in nw])
    nscore.append(len(cnw[i]))
    polarity.append((pscore[i] - nscore[i]) / ((pscore[i] + nscore[i]) + 0.000001))
    subjectivityscore.append((pscore[i] + nscore[i]) / ((len(without_sw[i])) + 0.000001))

masterDict['Positive_Words'], masterDict['Negative_Words'] = cpw, cnw



ppcount = []
wordcount = []
avgwordlength = []
avgSentenceLength = []
complexWordsPercent  =  []
Fog_Index = []
avgsyllablecount =[]
totalComplex = []


for file in os.listdir(scraped):
    with open(os.path.join(scraped, file),'r', encoding='ISO-8859-1') as f:
        read = f.read() 
        count = 0
        for pronoun in ["I", "we", "my", "ours", "us"]:
            count += len(re.findall(r"\b" + pronoun + r"\b", read))
        ppcount.append(count)
        
        read = re.sub(r'[^\w\s.]','',read)
        sentences = read.split('.')
        numsentences = len(sentences)
        words = [word  for word in read.split() if word.lower() not in stopwords.words('english') ]
        numwords = len(words)
        
 
        complexwords = []
        for word in words:
            syllablecountword = sum( 1 for letter in word if letter.lower() in 'aeiou')
            if syllablecountword > 2:
                complexwords.append(word)

        syllablecount = 0
        syllablewords =[]
        for word in words:
            if word.endswith('es'):
                word = word[:-2]
            elif word.endswith('ed'):
                word = word[:-2]
            syllableinword = sum( 1 for letter in word if letter.lower() in 'aeiou')
            if syllableinword >= 1:
                syllablewords.append(word)
                syllablecount += syllablecountword


    
    avgSLen = numwords / numsentences
    avgsyllablewordcount = syllablecount / len(syllablewords)
    complexPercent = len(complexwords) / numwords
    FogIndex = 0.4 * (avgSLen +  complexPercent)


    avgSentenceLength.append(slen)
    complexWordsPercent.append(complexpercent)
    Fog_Index.append(fog)
    totalComplex.append(complexcount)
    avgsyllablecount.append(avgsyllablewordcount)	



for file in os.listdir(scraped):
    with open(os.path.join(scraped,file), 'r', encoding='ISO-8859-1') as f:
        read = f.read()
        read = re.sub(r'[^\w\s]', '' , read)
        words = [word  for word in read.split() if word.lower() not in stopwords.words('english')]
        length = sum(len(word) for word in words)
        avgwordlen = length / len(words)

    wordcount.append(totalwords)
    avgwordlength.append(avgwordlen)   


output = pd.read_excel('Output Data Structure.xlsx')
output.drop([44-37,57-37,144-37], axis = 0, inplace=True)
#output.head()
variables = [pscore,
            nscore,
            polarity,
            subjectivityscore,
            avgSentenceLength,
            complexWordsPercent,
            Fog_Index,
            avgSentenceLength,
            totalComplex,
            wordcount,
            avgsyllablecount,
            ppcount,
            avgwordlength]


for i, var in enumerate(variables):
    output.iloc[:,i+2] = var

#print("output")
output.to_csv('output.csv')







