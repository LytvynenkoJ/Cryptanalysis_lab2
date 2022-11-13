import numpy as np
import math
import random
import pandas as pd
import heapq
import copy
import zlib

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
def split(L,N,step=50):
    splitedText=[]
    for i in range(N):
        splitedText.append(text[step*i: step*i+L])
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
        j=0
        while j <len(text[0]):
            temp = (a*alphabetS.find(text[i][j])+b)%(32**l)
            if l==1:
                dT+=alphabetS[temp]
                j+=1
            if l==2:
                dT+=alphabetS[temp//32]
                dT+=alphabetS[temp%32]
                j+=2
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
        j=0
        while j<L:
            temp = (s0+s1)%(32**l)
            if l==1:
                dT+=alphabetS[temp]
                s0=s1
                s1=temp
                j+=1
            if l==2:
                dT+=alphabetS[temp//32]
                dT+=alphabetS[temp%32]
                s0=s1
                s1=temp
                j+=1
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

#для критерію заборонених l-грам необхідні обрахунки:
#   -кількість входжень заборонених l-грам у тексті (для критеріїв 1.0 та 1.1)
#   -частоти заборонених l-грам (для критерію 1.2)
#   -сума частот заборонених l-грам (для критерію 1.3)
def CountForCriteria1(damaged_text, typ):
    N=len(damaged_text)
    result=[]
    counts=[]
    freqs=[]
    freqSum=[]
    if typ==1:
        for i in range(N):
            x=0
            for j in range(len(A[0])):
                if damaged_text[i].count(A[0][j])>0:
                    x += damaged_text[i].count(A[0][j])
                counts.append(damaged_text[i].count(A[0][j]))
                freqs.append(counts[-1]/len(damaged_text[i]))
            result.append(x)
            freqSum.append(x/len(damaged_text[i]))
    if typ==2:
        for i in range(N):
            x=0
            for j in range(len(A[1])):
                if damaged_text[i].count(A[1][j])>0:
                    x += damaged_text[i].count(A[1][j])
                counts.append(damaged_text[i].count(A[1][j]))
                freqs.append(counts[-1]/(len(damaged_text[i])-1))
            result.append(x)
            freqSum.append(x/(len(damaged_text[i])-1))
    return result, counts, freqs, freqSum

#критерії 1.0, 1.1 та 1.3 загалом мають однаковий вигляд тому об'єднуємо їх в одну функцію
def criteria1013(cfc, l):
    result=[]
    for i in range(len(cfc)):
        if cfc[i]>l:
            result.append(1)
        else:
            result. append(0)
    return result

#критерій 1.2 вийшов трошки корявий, але можливо згодом вигадаю як зробити його красивим
def criteria12(cfc, typ):
    result=[]
    if typ==1:
        coun = 0
        l=len(A[0])
        for i in range(len(cfc)):
            if i%l==0 and i!=0:
                if coun>0:
                    result.append(1)
                else:
                    result.append(0)
                coun=0
            fS = alphabetS.find(A[0][i%l])
            if cfc[i]>freq[fS]:
                coun+=1
        if coun>0:
            result.append(1)
        else:
            result.append(0)
    if typ==2:
        coun = 0
        l=len(A[1])
        for i in range(len(cfc)):
            if i%l==0 and i!=0:
                if coun>0:
                    result.append(1)
                else:
                    result.append(0)
                coun=0
            f1 = alphabetS.find(A[1][i%l][0])
            f2 = alphabetS.find(A[1][i%l][1])
            if cfc[i]>freqBigram[f1][f2]:
                coun+=1
        if coun>0:
            result.append(1)
        else:
            result.append(0)
    return result

#критерій 3.0
def criteria30(text, level):
    result1=[]
    result2=[]
    for i in range(len(text)):
        f = frequencies(text[i])
        ent=entropy(f[1],f[3])
        if abs(ent[0]-e[0])>level:
            result1.append(1)
        else:
            result1.append(0)
        if abs(ent[1]-e[1])>level:
            result2.append(1)
        else:
            result2.append(0)
    return result1, result2

#підрахунок найчастіших символів алфавіту та найчастіших біграм
def mostFreq(freqA, freqB, j1, j2):
    result=[]
    r=[]
    f=copy.deepcopy(freqA)
    for i in range(j1):
        maxIndex=f.index(max(f))
        r.append(alphabetS[maxIndex])
        f[maxIndex]=0
    result.append(r)
    r=[]
    f=copy.deepcopy(freqB)
    for i in range(j2):
        m=max([i for rows in f for i in rows])
        maxIndex=[(i,j) for i in range(32) for j in range(32) if f[i][j]==m]
        f[maxIndex[0][0]][maxIndex[0][1]]=0
        string=""
        string+=alphabetS[maxIndex[0][0]]
        string+=alphabetS[maxIndex[0][1]]
        r.append(string)
    result.append(r)
    return result

#критерій 5.1
def criteria51(text, level1, level2, mostFreq):
    result1=[]
    result2=[]
    for i in range(len(text)):
        r=[]
        for j in range(len(mostFreq[0])):
            r.append(text[i].count(mostFreq[0][j]))
        if r.count(0)>=level1:
            result1.append(1)
        else:
            result1.append(0)
        r=[]
        for j in range(len(mostFreq[1])):
            r.append(text[i].count(mostFreq[1][j]))
        if r.count(0)>=level2:
            result2.append(1)
        else:
            result2.append(0)
    return result1, result2

#будуємо дерево та знаходимо коди Хаффмана для кожного з символів алфавіту
class Tree:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left  = left
        self.right = right

    def __str__(self):
        return str(self.cargo)
    
    def __lt__(self, other):
        return self.freq < other.freq

def codingTree(node, sCode, huffCode):
    if node.left is None and node.right is None:
        if len(sCode)>0:
            huffCode[node.ch]=sCode
        else:
            huffCode[node.ch]='1'
        return
    codingTree(node.left, sCode + '0', huffCode)
    codingTree(node.right, sCode + '1', huffCode)
    
def huffman(text):
    freq = frequencies(text)[0]
    nodes=[Tree(alphabetS[i],freq[i]) for i in range(32) if freq[i]!=0]
    heapq.heapify(nodes)
    while(len(nodes)!=1):
        leftNode = heapq.heappop(nodes)
        rightNode = heapq.heappop(nodes)
        newNodeFreq=leftNode.freq+rightNode.freq
        heapq.heappush(nodes, Tree(None, newNodeFreq, leftNode, rightNode))
    huffCode={}
    codingTree(nodes[0], '', huffCode)
    return huffCode

#кодування в лоб
def binary(num):
    stringNum=""
    while num>0:
        if num%2==0:
            stringNum=f'{0}{stringNum}'
        else:
            stringNum=f'{1}{stringNum}'
        num=num//2
    return stringNum

def stupidCoding(text):
    freq = frequencies(text)[0]
    dictionary={alphabetS[i]: freq[i] for i in range(32)}
    sortedKey=sorted(dictionary, key=dictionary.get, reverse=True)
    codes={alphabetS[i]: '' for i in range(32)}
    n=1
    for i in sortedKey:
        codes[i]=binary(n)
        n+=1
    return codes

#функція кодування тексту довільним кодом, який буде надіслано на вхід
def textEncode(text, code):
    encodedT=""
    for i in text:
        encodedT+=code[i]
    return encodedT

#структурний критерій
def structCriteria(text, coding, level):
    result=[]
    damagedText=damage3(len(text[0]),len(text))
    for i in range(len(text)):
        temp = (len(text[i])*16)/len(textEncode(text[i], coding))
        compare = (len(damagedText[i])*16)/len(textEncode(damagedText[i], coding))
        if (abs(temp-compare)<level):
            result.append(1)
        else:
            result.append(0)
    return result

#похибки першого та другого роду
def alpha(cr):
    return sum(cr)/len(cr)
def beta(cr):
    return 1-sum(cr)/len(cr)

#тести для шифру Віженера
for r in [1,5,10]:
    print()
    print(r)
    for L in [10,100,1000,10000]:
        N=10000
        if L==10000:
            N=1000
        print("L = " + str(L)+ "        N = " + str(N))
        splitedText=split(L,N)
        damagedText=damage1(splitedText,r)
        cfc1=CountForCriteria1(splitedText, 1)
        cfc2=CountForCriteria1(damagedText, 1)
        cfc3=CountForCriteria1(splitedText, 2)
        cfc4=CountForCriteria1(damagedText, 2)
        
        #критерій 1.0
        cr=criteria1013(cfc1[0],0)
        print(" & 1.0  & " + str(alpha(cr)), end=' ')
        cr=criteria1013(cfc2[0],0)
        print("& " + str(beta(cr)), end=' ')
        cr=criteria1013(cfc3[0],0)
        print("& " + str(alpha(cr)), end=' ')
        cr=criteria1013(cfc4[0],0)
        print("& " + str(beta(cr)) + " \\\ ")
        
        
        #критерій 1.1
        cr=criteria1013(cfc1[0],(AFreqs[0]*L))
        print(" & 1.1  & " + str(alpha(cr)), end=' ')
        cr=criteria1013(cfc2[0],(AFreqs[0]*L))
        print(" & " + str(beta(cr)), end=' ')
        cr=criteria1013(cfc3[0],(AFreqs[1]*L))
        print(" & " + str(alpha(cr)), end=' ')
        cr=criteria1013(cfc4[0],(AFreqs[1]*L))
        print(" & " + str(beta(cr)) +" \\\ ")
        
        
        #критерій 1.2
        cr=criteria12(cfc1[2],1)
        print(" & 1.2  & " + str(alpha(cr)), end=' ')
        cr=criteria12(cfc2[2],1)
        print(" & " + str(beta(cr)), end=' ')
        cr=criteria12(cfc3[2],2)
        print(" & " + str(alpha(cr)), end=' ')
        cr=criteria12(cfc4[2],2)
        print(" & " + str(beta(cr)) +" \\\ ")
        
        
        #критерій 1.3
        cr=criteria1013(cfc1[3],AFreqs[0])
        print(" & 1.3  & " + str(alpha(cr)), end=' ')
        cr=criteria1013(cfc2[3],AFreqs[0])
        print(" & " + str(beta(cr)), end=' ')
        cr=criteria1013(cfc3[3],AFreqs[1])
        print(" & " + str(alpha(cr)), end=' ')
        cr=criteria1013(cfc4[3],AFreqs[1])
        print(" & " + str(beta(cr)) +" \\\ ")
        
        
        #критерій 3.0
        cr1=criteria30(splitedText, 0.05)
        print(" & 3.0  & " + str(alpha(cr1[0])), end=' ')
        cr2=criteria30(damagedText, 0.05)
        print(" & " + str(beta(cr2[0])), end=' ')
        print(" & " + str(alpha(cr1[1])), end=' ')
        print(" & " + str(beta(cr2[1])) +" \\\ ")
        
        
        #критерій 5.1 подобрать границы!!!!!
        mostF=mostFreq(freq, freqBigram, 3, 10)
        cr1=criteria51(splitedText, 2, 5)
        print(" & 5.1  & " + str(alpha(cr1[0])), end=' ')
        cr2=criteria51(damagedText, 2, 5)
        print(" & " + str(beta(cr2[0])), end=' ')
        print(" & " + str(alpha(cr1[1])), end=' ')
        print(" & " + str(beta(cr2[1])) +" \\\ ")
        
        
        #структурний критерій 1
        str1=structCriteria(splitedText, H, 1)
        print(" & структурний(1)  & " + str(alpha(str1)), end=' ')
        str2=structCriteria(damagedText, H, 1)
        print(" & " + str(beta(str2)) + " & " + str(alpha(str1))+ " & " + str(beta(str2)) + " \\\ ")
        
        
        #структурний критерій 2
        str1=structCriteria(splitedText, H2, 2)
        print(" & структурний(2)  & " + str(alpha(str1)), end=' ')
        str2=structCriteria(damagedText, H2, 2)
        print(" & " + str(beta(str2)) + " & " + str(alpha(str1))+ " & " + str(beta(str2)) + " \\\ \hline")
        
        print()
        print()
