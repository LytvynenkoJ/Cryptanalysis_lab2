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

#щоб далі було простіше присвоюємо результатам нормальні імена
f = frequencies(text)
coun=f[0]
freq=f[1]
countBigram=f[2]
freqBigram=f[3]

#таблиця кількостей символів алфавіту
print(pd.DataFrame(coun, index = alphabetS_list))

#таблиця частот символів алфавіту
print(pd.DataFrame(freq, index = alphabetS_list))

#таблиця кількостей біграм
print(pd.DataFrame(countBigram, columns = alphabetS_list, index = alphabetS_list))

#таблиця частот біграм
print(pd.DataFrame(freqBigram, columns = alphabetS_list, index = alphabetS_list))

#об'єднуємо в одну функцію підрахунок ентропії на символ джерела
def entropy(freq, freqB):
    entropy1=0
    for i in range(32):
        if freq[i]!=0:
            entropy1-=freq[i]*math.log2(freq[i])
        
    entropy2=0
    for i in range(32):
        for j in range(32):
            if freqB[i][j]!=0:
                entropy2-=freqB[i][j]*math.log2(freqB[i][j])
    entropy2/=2
    return entropy1, entropy2

#власне результат
e=entropy(freq,freqBigram)
print("entropy (l=1) :         "+str(e[0]))
print("entropy (l=2) :         "+str(e[1]))

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

#розбиття тексту на частини
def split(L,N):
    splitedText=[]
    for i in range(N):
        splitedText.append(text[i*L: (i+1)*L])            
    return splitedText

#перше спотворення тексту(шифр Віженера з випадковим ключем довжини r)
def damage1(text, r):
    key=[random.randint(0,32) for i in range(r)]
    damagedText=[]
    n=len(text)
    l=len(text[0])
    for i in range(n):
        dT=""
        for j in range(l):
            temp = (alphabetS.find(text[i][j])+key[j%r])%32
            dT+=alphabetS[temp]
        damagedText.append(dT)
    return damagedText

#алгоритм Евкліда
def euclid(a, b):
    if a == 0 :
        return b,0,1
    r,u,v = euclid(b%a, a)
    x = v - (b//a) * u
    y = u
    return r,x,y

#друге спотворення тексту (шифр афiнної та афiнної бiграмної пiдстановки з випадковими ключами)
def damage2(text,l):
    damagedText=[]
    gcd=2
    a=0
    while gcd>1:
        a=random.randint(1,32**l-1)
        gcd=euclid(a,32**l)[0]
    b=random.randint(1,32**l-1)
    for i in range(len(text)):
        dT=""
        for j in range(len(text[0])):
            temp = (a*alphabetS.find(text[i][j])+b)%(32**l)
            dT+=alphabetS[temp]
        damagedText.append(dT)
    return damagedText

#третій варіант спотворення тексту (рiвномiрно розподiлена послiдовнiсть символiв алфавіту)
def damage3(L, N):
    damagedText=[]
    for i in range(N):
        dT=""
        for j in range(L):
            temp = random.randint(0,31)
            dT+=alphabetS[temp]
        damagedText.append(dT)
    return damagedText

#четвертий варіант спотворення тексту (рекурента)
def damage4(L,N):
    damagedText=[]
    s0=random.randint(0,31)
    s1=random.randint(0,31)
    for i in range(N):
        dT=""
        for j in range(L):
            temp = (s0+s1)%32
            dT+=alphabetS[temp]
            s0=s1
            s1=temp
        damagedText.append(dT)
    return damagedText

#для критерію заборонених l-грам відповідно потрібно скласти список цих заборонених l-грам
#   список для літер (одразу ж підраховуємо суму частот заборонених l-грам)
A=[]
AFreqs=[0,0]
a1=[]
for i in range(32):
    if freq[i]<0.005:
        a1.append(alphabetS[i])
        AFreqs[0]+=freq[i]
A.append(a1)

#   та список для біграм (також одразу підраховуємо суму частот заборонених l-грам)
A2=[]
for i in range(32):
    for j in range(32):
        a2=""
        if freqBigram[i][j]==0:
            a2+=alphabetS[i]
            a2+=alphabetS[j]
            A2.append(a2)
            AFreqs[1]+=freqBigram[i][j]
A.append(A2)
