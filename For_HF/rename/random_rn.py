import os
import time
import random

path = "C:\\Tzu-Ling\\pytry\\forSH\\KDD_dataset_v2\\train"
# path = "C:\\Tzu-Ling\\pytry\\forSH\\KDD_dataset_v2\\test"


a1 = (2018,7,1,0,0,0,0,0,0)        #開始日期時間元祖（1976-01-01 00：00：00）
a2 = (2019,8,31,23,59,59,0,0,0)    #結束日期時間元祖（1990-12-31 23：59：59）

start = time.mktime(a1)    #生成開始時間戳
end = time.mktime(a2)      #生成結束時間戳

listSteth = []
listFA = []
for i in range(10000):      
    t = random.randint(start,end)    #在開始時間戳與結束時間戳之中隨機取出一個
    # print(t)
    date_touple = time.localtime(t)          #將時間戳生成時間元祖
    # print(date_touple)
    date = time.strftime("%Y%m%d",date_touple)  #將時間元祖轉成格式化字串（如1976-05-21）
    dateFA = time.strftime("%Y-%m-%d",date_touple)
    # append之前，應該先檢查random的值是否重覆!!!
    listSteth.append(date) # for 3M
    listFA.append(dateFA)  # for FA1
# print(listSteth)
# print(listSteth[0])
# print(listFA)


steWavDate_all = []
steTxtDate_all = []
faWavDate_all = []
faTxtDate_all = []
for roots, dirs, files in os.walk(path):
    for afile in files:
        fileName = str(os.path.join(roots, afile))  #完整路徑
        # print(fileName)
        afileName = str(afile)                      #只有檔名
        if "steth" in afileName and ".wav" in afileName:
            steWavDate = afileName[6:14]  #取出原檔案名稱裡的日期字串 # 20190820
            # print(steWavDate) 
            steWavDate_all.append(steWavDate)
        if "steth" in afileName and ".txt" in afileName:
            steTxtDate = afileName[6:14]
            # print(steTxtDate)
            steTxtDate_all.append(steTxtDate)
        if "trunc" in afileName and ".wav" in afileName: 
            faWavDate = afileName[6:16] # 2019-07-09
            # print(faWavDate) 
            faWavDate_all.append(faWavDate)
        if "trunc" in afileName and ".txt" in afileName:
            faTxtDate = afileName[6:16]
            faTxtDate_all.append(faTxtDate)
            # print(faTxtDate)
    print(len(steWavDate_all))
    # print(steWavDate_all)
    print(len(steTxtDate_all))
    print(len(faWavDate_all))
    print(faWavDate_all)
    print(len(faTxtDate_all))

    newDate = []
    b = 0
    # -----------------steWavDate_all--------所有ste要改成fa-----------
    for a in range(0,len(faWavDate_all)):  
        if str(faWavDate_all[a]) == str(faWavDate_all[a-1]):  # 若當日期和上一個檔案一樣
            # print('一樣')
            # print(steWavDate_all[a])
            # print(steWavDate_all[a-1])
            newDate.append(str(listFA[b]))   #這裡要改是FA還是3M
        elif str(faWavDate_all[a]) != str(faWavDate_all[a-1]):
            b += 1
            # print('不一樣')
            # print(steWavDate_all[a])
            # print(steWavDate_all[a-1])
            newDate.append(str(listFA[b]))
    print(newDate)  #for steWav and steTxt   #這569個新日期，要對應到3M.wav
    print(len(newDate))
    c = 0
    d = 0
    for bfile in files:
        if "trunc" in bfile and ".wav" in bfile:
            fileName2 = str(os.path.join(roots, bfile)) # 全部3M的完整路徑
            # print(fileName2)
            NewFileName = fileName2.replace(faWavDate_all[c],newDate[c])
            print(NewFileName)
            c = c+1
            print(c)
            os.rename(fileName2, NewFileName)
        if "trunc" in bfile and ".txt" in bfile:
            fileName2 = str(os.path.join(roots, bfile))
            NewFileName = fileName2.replace(faWavDate_all[d],newDate[d])
            print(NewFileName)
            os.rename(fileName2, NewFileName)
            d = d+1
            print(d)


