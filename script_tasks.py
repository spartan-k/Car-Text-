#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:35:23 2020

@author: paul-emile.gras
"""

import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer 

data=pd.read_csv('/Users/paul-emile.gras/Downloads/works.csv')

data1=data['comment']
data1=data1.dropna()
data1 = data1.sample(n=5000)
data1=data1.reset_index()
data1=data1['comment']

## Lowercase and tokenize
data2=data1
for i in range(0,5000):
    data2[i]=data1[i].lower()
    data2[i]=nltk.word_tokenize(data2[i])

## Remove stop words
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))

for i in range (0,5000):
    for w in data2[i]:
        if w in stopWords:
            data2[i].remove(w)

#### TASK A ####

## Import data on cars
cars=pd.read_csv('/Users/paul-emile.gras/Downloads/models.csv',encoding = 'unicode_escape')

## Create the dictionary with the unique brand models
brands=cars['brand']
brands=brands.drop_duplicates()
models=cars['model']

#replace model names with brand names
data_a=data2
for i in range (0,5000):
    n=len(data_a[i])
    for j in range (0,n):
        word=data_a[i][j]
        if word in models:
            temp=cars[cars.model==word]
            temp_brand=temp.iloc[0,0]
            data_a[i][j]=temp_brand

#get frequency
freq={}
for brand in brands:
    freq[brand]=0

list_brands=[]
for brand in brands:
    list_brands.append(brand)
list_brands

for i in range (0,5000):
    temp=list(dict.fromkeys(data_a[i]))
    for word in temp:
        if word in list_brands:
            freq[word]+=1
freq

ten_brands = []
for key, value in sorted(freq.items(), key=lambda item: item[1],reverse = True):
    ten_brands.append(key)
ten_brands = ten_brands[1:13]
ten_brands.remove('problem')
ten_brands.remove('seat')
ten_brands # List of top 10 brands by frequency

## Add double mentions to compute lift ratios

#Initialize the dictionary of frequencies
freq_bis={}
for i in range(10):
    brand1=ten_brands[i]
    freq_bis[brand1]=0
    for j in range(i+1,10):
        brand2=ten_brands[j]
        freq_bis[brand1+'&'+brand2]=0
freq_bis

#Populate the dictionary of frequencies
for k in range (0,5000):
    comment=list(dict.fromkeys(data_a[k]))
    
    #Initialize brand_in_comment (b_in_c) dictionary
    b_in_c={} #brand in comment?
    for brand in ten_brands:
        b_in_c[brand]=0
    
    #Check which brands are in the comment
    for brand in ten_brands:
        if brand in comment:
            b_in_c[brand]=1
    
    #adjust freq_bis wfor the brands in the comment
    for i in range(10):
        brand1=ten_brands[i]
        if b_in_c[brand1]==1:
            freq_bis[brand1]+=1
        for j in range(i+1,10):
            brand2=ten_brands[j]
            if b_in_c[brand1]==1 and b_in_c[brand2]==1:
                freq_bis[brand1+'&'+brand2]+=1

freq_bis

## Create the lift ratios matrix

lift_ratios=pd.DataFrame(index=ten_brands,columns=ten_brands)
for i in range(10):
    brand1=ten_brands[i]
    for j in range(i+1,10):
        brand2=ten_brands[j]
        lift_ratios[brand2][brand1]=(5000*freq_bis[brand1+'&'+brand2])/(freq_bis[brand1]*freq_bis[brand2])
        lift_ratios[brand1][brand2]=(5000*freq_bis[brand1+'&'+brand2])/(freq_bis[brand1]*freq_bis[brand2])

for i in range (10):
    for j in range(10):
        if np.isnan(lift_ratios.iloc[i,j]):
            lift_ratios.iloc[i,j]=1        

## MDS

from sklearn import manifold
import matplotlib.pyplot as plt

mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=6)
results = mds.fit(lift_ratios)

brands_bis = lift_ratios.columns
coords = results.embedding_

fig = plt.figure()#figsize=(12,10))

plt.subplots_adjust(bottom = 0.1)
plt.scatter(coords[:, 0], coords[:, 1],color='turquoise')

for label, x, y in zip(brands_bis, coords[:, 0], coords[:, 1]):
    plt.annotate(
        label,
        xy = (x, y), 
        xytext = (-20, 20),
        textcoords = 'offset points'
    )
plt.show()

#### Task B ####
#See report

#### Task C ####

## Import data on attributes
attributes=pd.read_csv('/Users/paul-emile.gras/Downloads/attributes_k.csv') #,encoding = 'unicode_escape')
attributes=attributes.rename(columns={"brand_image": "subtype", "brand": "adjective"})

## Create the dictionary with the unique brand models
subtypes=attributes['subtype']
subtypes=subtypes.drop_duplicates()
adjectives=attributes['adjective']

## Replace adjectivees with subtypes
data_c=data_a #data with models replaced by brands
for i in range (0,5000):
    comment=data_c[i]
    n=len(comment)
    for j in range (0,n):
        word=comment[j]
        if word in list(adjectives):
            temp=attributes[attributes.adjective==word]
            temp_subtype=temp.iloc[0,0]
            data_c[i][j]=temp_subtype

## Get frequency
freq_b={}
for subtype in subtypes:
    freq_b[subtype]=0

list_subtypes=[]
for subtype in subtypes:
    list_subtypes.append(subtype)
list_subtypes

for i in range (0,5000):
    comment=list(dict.fromkeys(data_c[i]))
    for word in comment:
        if word in list_subtypes:
            freq_b[word]+=1
freq_b

## Get the 5 most frequent subtypes
five_subtypes = []
for key, value in sorted(freq_b.items(), key=lambda item: item[1],reverse = True):
    five_subtypes.append(key)
five_subtypes=five_subtypes[0:5]
five_subtypes

## Find the attributes associated with the 5 mpost frequent brands
five_brands=ten_brands[0:5]

## BMW
freq_bmw={}
for subtype in subtypes:
    freq_bmw[subtype]=0

for i in range (0,5000):
    comment=list(dict.fromkeys(data_c[i]))
    if 'bmw' in comment:
        for word in comment:
            if word in list_subtypes:
                freq_bmw[word]+=1

lift_ratios_bmw=freq_bmw
for attribute in freq_bmw.keys():
    lift_ratios_bmw[attribute]=5000*freq_bmw[attribute]/(freq['bmw'])*freq_b[attribute]

five_subtypes_bmw = []
for key, value in sorted(lift_ratios_bmw.items(), key=lambda item: item[1],reverse = True):
    five_subtypes_bmw.append(key)
five_subtypes_bmw=five_subtypes_bmw[0:5]
five_subtypes_bmw


## Sedan
freq_sedan={}
for subtype in subtypes:
    freq_sedan[subtype]=0

for i in range (0,5000):
    comment=list(dict.fromkeys(data_c[i]))
    if 'sedan' in comment:
        for word in comment:
            if word in list_subtypes:
                freq_sedan[word]+=1

lift_ratios_sedan=freq_sedan
for attribute in freq_sedan.keys():
    lift_ratios_sedan[attribute]=5000*freq_sedan[attribute]/(freq['sedan'])*freq_b[attribute]

five_subtypes_sedan = []
for key, value in sorted(lift_ratios_sedan.items(), key=lambda item: item[1],reverse = True):
    five_subtypes_sedan.append(key)
five_subtypes_sedan=five_subtypes_sedan[0:5]
five_subtypes_sedan

## Acura
freq_acura={}
for subtype in subtypes:
    freq_acura[subtype]=0

for i in range (0,5000):
    comment=list(dict.fromkeys(data_c[i]))
    if 'acura' in comment:
        for word in comment:
            if word in list_subtypes:
                freq_acura[word]+=1

lift_ratios_acura=freq_acura
for attribute in freq_acura.keys():
    lift_ratios_acura[attribute]=5000*freq_acura[attribute]/(freq['acura'])*freq_b[attribute]

five_subtypes_acura = []
for key, value in sorted(lift_ratios_acura.items(), key=lambda item: item[1],reverse = True):
    five_subtypes_acura.append(key)
five_subtypes_acura=five_subtypes_acura[0:5]
five_subtypes_acura

## Audi
freq_audi={}
for subtype in subtypes:
    freq_audi[subtype]=0

for i in range (0,5000):
    comment=list(dict.fromkeys(data_c[i]))
    if 'audi' in comment:
        for word in comment:
            if word in list_subtypes:
                freq_audi[word]+=1

lift_ratios_audi=freq_audi
for attribute in freq_audi.keys():
    lift_ratios_audi[attribute]=5000*freq_audi[attribute]/(freq['audi'])*freq_b[attribute]

five_subtypes_audi = []
for key, value in sorted(lift_ratios_audi.items(), key=lambda item: item[1],reverse = True):
    five_subtypes_audi.append(key)
five_subtypes_audi=five_subtypes_audi[0:5]
five_subtypes_audi

## Infiniti

freq_infiniti={}
for subtype in subtypes:
    freq_infiniti[subtype]=0

for i in range (0,5000):
    comment=list(dict.fromkeys(data_c[i]))
    if 'infiniti' in comment:
        for word in comment:
            if word in list_subtypes:
                freq_infiniti[word]+=1

lift_ratios_infiniti=freq_infiniti
for attribute in freq_infiniti.keys():
    lift_ratios_infiniti[attribute]=5000*freq_infiniti[attribute]/(freq['infiniti'])*freq_b[attribute]

five_subtypes_infiniti = []
for key, value in sorted(lift_ratios_infiniti.items(), key=lambda item: item[1],reverse = True):
    five_subtypes_infiniti.append(key)
five_subtypes_infiniti=five_subtypes_infiniti[0:5]
five_subtypes_infiniti

print('bmw',five_subtypes_bmw,
      '\n sedan',five_subtypes_sedan,
      '\n acura',five_subtypes_acura,
      '\n audi',five_subtypes_audi,
      '\n infiniti',five_subtypes_infiniti)

#### Task D ####
#See report

#### Task E ####

## Import aspirational words
aspirational=pd.read_csv('/Users/paul-emile.gras/Downloads/aspirational_words.csv')

data_e = data_a #data with models replaced by brands
lemmatizer = WordNetLemmatizer() 

for i in range(0,1):    
    for j in range(0,len(data_e[i])): 
        data_e[i][j] = lemmatizer.lemmatize(data_e[i][j])

for i in range(0,len(aspirational['word'])):
    aspirational['word'][i] = lemmatizer.lemmatize(aspirational['word'][i])
    
freq_e={}
for brand in brands:
    freq_e[brand]=0

for k in range(0,5000):
    comment=list(dict.fromkeys(data_e[k]))
    #Number of aspirational words in the comment
    count=0
    for word in comment:
        if word in aspirational:
            count+=1
    #Add the count for the brands in the comment
    for brand in brands:
        if brand in comment:
            freq_e[brand]+=count
freq_e

aspirational_brands = []
for key, value in sorted(freq_e.items(), key=lambda item: item[1],reverse = True):
    aspirational_brands.append(key)
aspirational_brand=aspirational_brands[0] 
aspirational_brand #this is BMW


