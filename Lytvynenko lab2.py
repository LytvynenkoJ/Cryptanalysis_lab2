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
#одночасно з цим підраховуємо кількість кожного з символів алфавіту
freq=[0 for j in range(32)]
coun=[0 for j in range(32)]
file = open("text2.txt", "w", encoding="utf8")
for i in range(len(text)):
    fS = alphabetS.find(text[i])
    fB = alphabetB.find(text[i])
    if fS!=-1:
        coun[fS]+=1
        file.write(alphabetS[fS])
    if fB!=-1:
        coun[fS]+=1
        file.write(alphabetS[fB])
file.close()
