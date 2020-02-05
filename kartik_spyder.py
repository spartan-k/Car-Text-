## Text Analytics - Assignment 2


import pandas as pd
import numpy as np
import nltk

data=pd.read_csv(r'C:\Users\DELL\OneDrive - McGill University\Text Analytics_group\works.csv')
print(data.shape)

data1=data['comment']
data1=data1.dropna()
data1 = data1.sample(n=5000)
data1=data1.reset_index()
data1=data1['comment']

## Lowercase
data2=data1
for i in range(0,5000):
    data2[i]=data1[i].lower()

## Tokenize
for i in range(0,5000):
    data2[i]=nltk.word_tokenize(data2[i]) 

## Remove punctuation
#from nltk.tokenize import RegexpTokenizer
#tokenizer = RegexpTokenizer(r'\w+')
#for i in range(0,5000):
#    data2[i]=tokenizer.tokenize(data2[i])

## Remove stop words
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))

for i in range (0,5000):
    for w in data2[i]:
        if w in stopWords:
            data2[i].remove(w)

## Import data on cars
cars=pd.read_csv(r'C:\Users\DELL\OneDrive - McGill University\Text Analytics_group\models.csv',encoding =  'unicode_escape')

## Create the dictionary with the unique brand models
brands=cars['brand']
brands=brands.drop_duplicates()
models=cars['model']

#replace model names with brand names
data3=data2
for i in range (0,5000):
    n=len(data3[i])
    for j in range (0,n):
        word=data3[i][j]
        if word in models:
            temp=cars[cars.model==word]
            temp_brand=temp.iloc[0,0]
            data3[i][j]=temp_brand

#get frequency
freq={}
for brand in brands:
    freq[brand]=0

list_brands=[]
for brand in brands:
    list_brands.append(brand)
list_brands

for i in range (0,5000):
    temp=list(dict.fromkeys(data3[i]))
    for word in temp:
        if word in list_brands:
            freq[word]+=1
freq
taska = []
for key, value in sorted(freq.items(), key=lambda item: item[1],reverse = True):
    taska.append(key)
taska = taska[1:14]
taska.remove('problem')
taska.remove('seat')
taska.remove('sedan')

taska # List of top 10 brands by frequency

#Calculating lift ratio
count_taska = {}
for i in taska:
    count_taska[i] = 0
#j = 0


for j in range(0,9):
    for step in range(1,10-j):
        counter_j = 0
        counter_j1 = 0
        for i in range (0,5000):
            temp=data3[i]
            count_taska[taska[j]+taska[j+step]] = 0
            
            for word in temp:
                if word == taska[j]:
                    count_taska[taska[j]]+=1
                    counter_j += 1
                elif word == taska[j+step]:
                    count_taska[taska[j+step]]+=1
                    counter_j1 += 1
            if(counter_j >0 and counter_j1 > 0):
                count_taska[taska[j]+taska[j+step]] = counter_j1+ counter_j
lift_matrix = np.zeros((10,10))

j = -1
k = -1
for w1 in taska:
    j = j+1
    for w2 in taska:
        k = k+1
        if(w1 != w2):
            try:
                lift_matrix[j][k] = (5000*count_taska[w1+w2])/(count_taska[w1]*count_taska[w2])
            except Exception:
                pass
    k = -1        
    
#Import Attributes
attributes=pd.read_csv(r'C:\Users\DELL\OneDrive - McGill University\Text Analytics_group\attributes_k.csv')

#Replacing attributes with subtype
attributes['brand_image']

data4 = data3
attribute_name = list(attributes['brand'])
attribute_type = list(attributes['brand_image'])
for i in range (21,5000):
    
    n=len(data4[i])
    for j in range (0,n):
        
        word=data4[i][j]
        
        for k in range(0,199):
            
            if (word == attribute_name[k]):
                data4[i][j] = attribute_type[k]
                
 #Frequency
#get frequency
freq_att={}
for att2 in attribute_type:
    freq_att[att2]=0

list_atttype=[]
for att4 in attribute_type:
    list_atttype.append(att4)
list_atttype

for i in range (0,5000):
    temp1 = data4[i]
    temp=list(dict.fromkeys(temp1))
    for word in temp:
        if word in list(attribute_type):
            freq_att[word]+=1                   
                
                  
              
      

#------------------------------------------------------------------------
## Tokenize
import nltk
for i in range(0,5000):
    data2[i]=nltk.word_tokenize(data2[i])
    
brand_car=cars[cars.model=='integra']

print(cars['brand'][cars[cars['model'] == 'Legend'].index.tolist()].tolist())
#------------------------------------------------------------------------