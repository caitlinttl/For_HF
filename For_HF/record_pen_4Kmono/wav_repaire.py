# Python bytecode 3.7.3
# pydub http://builds.libav.org/windows/nightly-gpl/?C=M&O=D
# set path: ....C:\Users\tz\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\libav-i686-w64-mingw32-20180108\usr\bin
# Use pydub to 4000Hz and mono

import os
import time
import datetime
from pydub import AudioSegment

datapath = str(input(r'請輸入檔案資料夾路徑: '))

startdate = datetime.datetime.now()
t0 = time.perf_counter()

# dir = ('C:\\Tzu-Ling\\pytry\\wavmono\\test\\')
# dir = ('G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[FA1實驗紀錄]-[影音   彙整  報告 ]\\[FA1]-[臨床]-[20191115]-[和信]\\[FA1]-[臨床]-[20191115]-[錄音檔]\\')

dir = datapath + r'\\'

wavNum = 0

def WavResmMono(dir):
    global wavNum
    allfiles = os.listdir(dir)
    for file in allfiles:  
        filepath = os.path.join(dir,file)
        if os.path.isdir(filepath):
            WavResmMono(filepath)
        elif os.path:
            if '.wav' in os.path.basename(file):
                if ('_4K_mono.wav') in os.path.basename(file):
                    continue
                if os.path.exists (f'{(os.path.join(dir,file))[:-4]}_4K_mono.wav'):
                    continue
                wavNum +=1
                sound = AudioSegment.from_wav(str(dir)+str(file))
                sound = sound.set_channels(1)
                sound = sound.set_frame_rate(4000)
                sound.export(str(dir)+str(os.path.splitext(file)[0]) +'.wav', format="wav")  
                print(os.path.splitext(file)[0])
            
                      
WavResmMono(dir)


enddate = datetime.datetime.now()
t1 = time.perf_counter()
t_delta = t1-t0


print()
print('-------------------------REPORT-------------------------')
print()
print(f'Calculating  time: {t_delta:.2f} seconds '+"("+str(enddate-startdate)+")")
print('Start        time: '+startdate.strftime('%Y-%m-%d %H:%M:%S %a'))
print('End          time: '+enddate.strftime('%Y-%m-%d %H:%M:%S %a'))
print()
print('Total proscess_wav number: ',str(wavNum))
print()
print('-----------------------END(๑¯∀¯๑)-----------------------')
print()










