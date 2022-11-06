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