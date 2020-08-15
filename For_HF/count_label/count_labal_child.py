# Python bytecode 3.7 (3392)
# case number ONLY for trachra sound !!!!!
# Check ignoreNum when new-trachea-data add !!!!!!

ignoreNum = 2 #20191115計算次數為13 #由總表手工算 (目前會遇到同一個病人有多個音檔的問題，還有5min搗蛋的問題)

import datetime
import time
import os

startdate = datetime.datetime.now()
#start = time.time()
t0 = time.perf_counter()

NoiseNum = 0
ConNum = 0
In = 0
Ex = 0

def countFileLines(filename):
    count=0
    global NoiseNum
    global ConNum
    global In
    global Ex
    handle = open(filename)
    for line in handle:
        if 'Noise' in line:
            NoiseNum+=1
        if 'Conti' in line:
            ConNum+=1
        if 'Ins' in line:
            In+=1
        if 'Exp' in line:
            Ex+=1
        count+=1
    return count
 
wavNum = 0
firstcutNum = 0
txtNum = 0

def listdir(dir,lines):
    global wavNum
    global firstcutNum
    global txtNum
    files = os.listdir(dir)  #列出目錄下的所有文件和目錄
    for file in files:
        filepath = os.path.join(dir,file)
        if os.path.isdir(filepath):  #如果filepath是目錄，遞歸遍歷子目錄
           listdir(filepath,lines)
        elif os.path:   #如果filepath是文件，直接統計行數
            if os.path.splitext(file)[1]=='.txt' :
                txtNum +=1
                lines.append(countFileLines(filepath))
                print(file + ':'+str(countFileLines(filepath)))   #輸出此行造成sub_label數量要除二
            if os.path.splitext(file)[1]=='.wav' :
                wavNum+=1
            if '_0.wav' in os.path.basename(file) :
        #print(os.path.basename(file))
                firstcutNum+=1

            

lines = []
#dir = 'G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[已標註聲音]\\[已標註]-[FA1 data]'
#listdir(dir,lines)
#dir = 'G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[已標註聲音]\\[已標註]-[3M data]'
#listdir(dir,lines)
# dir = 'G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[已標註聲音]\\[已標註]-[喉音]\\'
# dir = 'G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[已標註聲音]\\[已標註]-[喉音]\\大人喉音\\'
dir = 'G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[已標註聲音]\\[已標註]-[喉音]\\小兒喉音\\'
listdir(dir,lines)

#dir = 'C:\\Tzu-Ling\\pytry\\txt\\20191111am-snoopy19890119'   #for test
#listdir(dir,lines)      


recordtime = wavNum*10 + firstcutNum*5
#檔名結尾為_0.wav的數量 = (原始音檔未切檔的音檔數量)  
#但因為切檔不足15秒則不切，所以實際收音時間會比算出來的時間多一點點，誤差少於 _0.wav數量*15秒
#原始音檔秒數 = 音檔數量*15 -音檔數量*5  + _0.wav數量*5 = 【 overlap切完後的音檔數量*10 + _0.wav數量*5 】
#每一個都重複5秒鐘，只有_0.wav不重複
#E.g. 原本有75秒 overlap5秒切完變成7個音檔(共105秒)
#75 = 7 *10 +5 =75  也可以等於 (7*15 -15) /1.5 +15 

m, s = divmod(recordtime, 60)
h, m = divmod(m, 60)
#print('%d:%02d:%02d' % (h, m, s))


caseNum = firstcutNum - ignoreNum  #人次 = _0.wav數量 - 多餘的_0.wav數量

                                        
enddate = datetime.datetime.now()
#end = time.time()
t1 = time.perf_counter()
t_delta = t1-t0

print('')
print('--------------------------TIME--------------------------')
print('')
print(f'Calculating  time: {t_delta:.2f} seconds '+"("+str(enddate-startdate)+")")
print('Start        time: '+startdate.strftime('%Y-%m-%d %H:%M:%S %a'))
print('End          time: '+enddate.strftime('%Y-%m-%d %H:%M:%S %a'))

print('')
print('-------------------------REPORT-------------------------')

print('')
print(startdate.strftime('%Y-%m-%d %H:%M:%S %a'))
print('')
print('Total counts: '+ '【' + str(sum(lines))+ '】')
print('Insp  counts: ' + str(int(In*1/2)))
print('Exp   counts: ' + str(int(Ex*1/2)))
print('Conti counts: ' + str(int(ConNum*1/2)))
print('Noise counts: ' + str(int(NoiseNum*1/2)))

print('')
print('Total case number: ' + str(caseNum))  
print('Total record time: ' + '%d:%02d:%02d' % (h, m, s))  #還沒做overlap5秒鐘切15秒檔的音檔總長度，切檔時剩餘秒數不足15秒則捨棄
print('')
#print('raw_wav     number: ' + str(firstcutNum))              #檔名結尾為_0.wav的數量 (原始音檔未切檔的音檔數量) 但又有5min那些在搗蛋
print('Trunc_wav number: ' + str(wavNum) + ' (duration 15sec, overlap 5sec)')                   #總wav數量  (切完檔的wav數量)
print('Label_wav number: ' +str(txtNum))
print('')

# for copy 

print('-----Child--------------for copy-------------------------')
print('')
print('')
print(str(sum(lines)))
print(str(int(In*1/2)))
print(str(int(Ex*1/2)))
print(str(int(ConNum*1/2)))
print('')
print('')
print('')
print('')
print(str(int(NoiseNum*1/2)))
print(str(caseNum))  
print('%d:%02d:%02d' % (h, m, s))  #還沒做overlap5秒鐘切15秒檔的音檔總長度，切檔時剩餘秒數不足15秒則捨棄
print('')
print('')


#rint('--------------------ya!!cheer up^^!!--------------------')
print('-----------------------END(๑¯∀¯๑)-----------------------')
print('')





#print(str(lines))

#print(f'start time: {start:.2f}')
#print(f'end time: {end:.2f}')
#print(f'calculating time: {end-start:.2f}')

#print('calculating time: '+str(enddate-startdate))
#print('calculating time: '+str((enddate-startdate).seconds))
#print('calculating time: %.2f seconds'%(end-start))
#print('start time: '+startdate.strftime('%Y-%m-%d %H:%M:%S %A'))
#print('end time: '+enddate.strftime('%Y-%m-%d %H:%M:%S %A'))

