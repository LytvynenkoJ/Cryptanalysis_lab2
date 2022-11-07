import numpy as np
import math
import random
import pandas as pd

#зчитуємо файл
file = open("text.txt", "r", encoding="utf8")
text=file.read()
file.close()

#український алфавіт з великими та малими літерами
alphabetS="абвгдеєжзиіїйклмнопрстуфхцчшщьюя"
alphabetB="АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
alphabetS_list = list(alphabetS)

#опрацьовуємо текст: позбавляємось від символів, які не входять до алфавіту
#   та замінюємо великі літери на малі
file = open("text2.txt", "w", encoding="utf8")
for i in range(len(text)):
    fS = alphabetS.find(text[i])
    fB = alphabetB.find(text[i])
    if fS!=-1:
        file.write(alphabetS[fS])
    if fB!=-1:
        file.write(alphabetS[fB])
file.close()

#зчитуємо вже виправлений файл (без великих літер та спецсимволів) з яким надалі будемо працювати
file = open("text2.txt", "r", encoding="utf8")
text=file.read()
file.close()

#об'єдуємо в одну функцію підрахуно кількості та частот символів алфавіту та біграм
def frequencies(text):
    coun=[0 for j in range(32)]
    for i in range(len(alphabetS)):
        coun[i]=text.count(alphabetS[i])
    s=sum(coun)
    freq=[0 for j in range(32)]
    for i in range(len(coun)):
        freq[i]=coun[i]/s
    
    s=0
    countBigram=[[0 for j in range(32)] for i in range(32)]
    for i in range(len(text)):
        find1 = alphabetS.find(text[i])
        if i+1<len(text):
            find2 = alphabetS.find(text[i+1])
            countBigram[find1][find2]+=1
            s+=1
    freqBigram=[[0 for j in range(32)] for i in range(32)]
    for i in range(32):
        for j in range(32):
            freqBigram[i][j]=countBigram[i][j]/s
    return coun, freq, countBigram, freqBigram

#таблиця кількостей символів алфавіту
print(pd.DataFrame(coun, index = alphabetS_list))

#таблиця частот символів алфавіту
print(pd.DataFrame(freq, index = alphabetS_list))

#таблиця кількостей біграм
print(pd.DataFrame(countBigram, columns = alphabetS_list, index = alphabetS_list))

#таблиця частот біграм
print(pd.DataFrame(freqBigram, columns = alphabetS_list, index = alphabetS_list))

#ентропія на символ джерела (l=1)
entropy=0
for i in range(32):
    entropy-=freq[i]*math.log2(freq[i])
print("entropy (l=1) :         "+str(entropy))

#ентропія на символ джерела (l=2)
entropyBigram=0
for i in range(32):
    for j in range(32):
        if freqBigram[i][j]!=0:
            entropyBigram-=freqBigram[i][j]*math.log2(freqBigram[i][j])
entropyBigram/=2
print("entropy (l=2) :         "+str(entropyBigram))

#індекс відповідності (l=1)
index=0
for i in range(32):
    index+=coun[i]*(coun[i]-1)
index/=len(text)*(len(text)-1)
print("index (l=1) :         "+str(index))


#індекс відповідності (l=2)
indexBigram=0
for i in range(32):
    for j in range(32):
        if countBigram[i][j]!=0:
            indexBigram+=countBigram[i][j]*(countBigram[i][j]-1)
indexBigram/=len(text)*(len(text)-1)
print("index (l=2) :         "+str(indexBigram))
