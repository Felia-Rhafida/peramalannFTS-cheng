import pandas as pd
import math
from collections import Counter
import numpy as np

def Semesta(Data, D1, D2):
    semesta = [min(Data) - D1, max(Data) + D2]
    return semesta
    
def Interval(Data, D1, D2):
    rentang = (max(Data) + D2) - (min(Data) - D1)
    n = len(Data)
    K = 1 + 3.322 * math.log10(n)
    I = round(rentang / K)
    qtyInterval = round(rentang / I)
    return rentang, K, I, qtyInterval
    
def HimpunanFuzzy(I, qtyInterval, dmin):
    kelas = []
    bBawah = []
    bAtas = []
    nTengah = []
    nilai = dmin
    dataDict = {}
    for i in range(1, qtyInterval + 1):
        kelas.append("A" + str(i))
        batasBawah = nilai
        batasAtas = nilai + I
        nilaiTengah = (batasBawah + batasAtas) / 2
        bBawah.append(int(batasBawah))
        bAtas.append(int(batasAtas))
        nTengah.append(int(nilaiTengah))
        nilai = batasAtas
    for i in range(0, len(kelas)):
        dataDict[kelas[i]] = {"nilai": nTengah[i]}
    return kelas, bBawah, bAtas, nTengah, dataDict

def Fuzzifikasi(kelompok, kelas, data):
    fuzzifikasi = []
    for nilai in data:
        for i, k in enumerate(kelompok):
            if nilai < k:
                fuzzifikasi.append(kelas[i])
                break
    return fuzzifikasi

def FuzzyLogicRelation(fuzzifikasi):
    flr = []
    for i in range(len(fuzzifikasi)):
        if i < 1:
            flr.append(f">> {fuzzifikasi[i]}")
        else:
            flr.append(f"{fuzzifikasi[i-1]} >> {fuzzifikasi[i]}")
    return flr

def FLRGroup(data):
    dictFLRG = {}
    for i in range(len(data) - 1):
        current_state = data[i]
        next_state = data[i + 1]
        if current_state not in dictFLRG:
            dictFLRG[current_state] = []
        dictFLRG[current_state].append(next_state)
    for current_state, next_states in dictFLRG.items():
        dictFLRG[current_state] = list(next_states) 
    return dictFLRG

def Pembobotan(data):
    flrg = []
    bobot = []
    pembobotan = []
    for i in data:
        element_count = Counter(i)
        result = list(element_count.values())
        result2 = list(element_count.keys())
        bobot.append(result)
        flrg.append(result2)
        comper = [round((x / sum(result)), 2) for x in result]
        pembobotan.append(comper)
    return bobot, pembobotan , flrg

def Defuzzikasi(flrgroup, bobot, newflrg):
    key = flrgroup.keys()
    list_key = list(key) 
    deffuzikasi = []
    dictDeffuzikasi = {}
    flrgnew = []
    for i in range(len(newflrg)):
        row = []
        for j in range(len(newflrg[i])):
            if newflrg[i][j] in dataDict:
                row.append(dataDict[newflrg[i][j]]['nilai'])
        flrgnew.append(row)
    for i in range(len(flrgnew)):
        row = []
        for j in range(len(flrgnew[i])):
            result = flrgnew[i][j] * bobot[i][j]
            row.append(round(result))
        deffuzikasi.append(row)
    for i in range(len(deffuzikasi)):
        dictDeffuzikasi[list_key[i]] = sum(deffuzikasi[i])
    return dictDeffuzikasi

def Peramalan(fuzzifikasi, deffuzikasi):
    peramlan = []
    for i in fuzzifikasi:  
        peramlan.append(deffuzikasi[i])
    return peramlan
    
def mean_absolute_percentage_error(actual_values, predicted_values): 
    actual_values, predicted_values = np.array(actual_values), np.array(predicted_values)
    n = len(actual_values)
    mape = (1/n) * sum(abs((actual_values[i] - predicted_values[i]) / actual_values[i]) * 100 for i in range(n))
    return mape

file_path = 'C:/Users/Lenovo/Documents/fts cheng/bismillah2.xlsx'
df = pd.read_excel(file_path)
time_series_column = 'MPW'
D1= 1
D2= 1

semesta = Semesta(df[time_series_column], D1=D1, D2=D2)
rentang, K, I, qty_interval = Interval(df[time_series_column], D1=D1, D2=D2)
kelas, bBawah, bAtas, nTengah, dataDict = HimpunanFuzzy(I, qty_interval, min(df[time_series_column]))
kelompok = bAtas
fuzzifikasi = Fuzzifikasi(kelompok, kelas, df[time_series_column])
flr = FuzzyLogicRelation(fuzzifikasi)
flr_grouped = FLRGroup(fuzzifikasi)
bobot, pembobotan, flrg = Pembobotan(flr_grouped.values())
deffuzikasi= Defuzzikasi(flr_grouped, pembobotan, flrg)
peramalan = Peramalan(fuzzifikasi, deffuzikasi)
mape = mean_absolute_percentage_error(df[time_series_column], peramalan)
mape_percentage = f"{mape:.2f}%"

print(f"Himpunan Semesta Fuzzy (U): {semesta}")
print(f"Rentang: {rentang}")
print(f"K: {K}")
print(f"Interval: {I}")
print(f"Jumlah Interval: {qty_interval}")
print(f"Kelas: {kelas}")
print(f"Batas Bawah: {bBawah}")
print(f"Batas Atas: {bAtas}")
print(f"Nilai Tengah: {nTengah}")
print("Data Dictionary:")
for key, value in dataDict.items():
    print(f"{key}: {value}")
print(f"Fuzzifikasi: {fuzzifikasi}")
print(f"Fuzzy Logic Relation: {flr}")
print("FLRG:")
for key, value in flr_grouped.items():
    print(f"{key}: {value}")
print(f"Bobot: {bobot}")
print(f"Pembobotan: {pembobotan}")
print(f"flrg: {flrg}")
print(f"Defuzzifikasi: {deffuzikasi}")
print(f"peramalan: {peramalan}")
print(f'MAPE: {mape_percentage}')

nilai_terakhir_1 = peramalan[-1:]
jumlah_periode_ke_depan = 4
peramalan_4_periode_ke_depan = []
for i in range(jumlah_periode_ke_depan):
    nilai_minggu_depan = nilai_terakhir_1[-1]  
    peramalan_4_periode_ke_depan.append(nilai_minggu_depan)
    nilai_terakhir_1 = nilai_terakhir_1[-1:] + [nilai_minggu_depan]
print(f"Perkiraan nilai untuk periode 4 minggu periode ke depan: {peramalan_4_periode_ke_depan}")