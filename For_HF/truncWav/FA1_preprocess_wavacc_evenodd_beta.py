# ====== ACC [for labelling] trauncate 15sec WAV every 2 mins 
import soundfile as sf
import os
import json
import csv
from sklearn.decomposition import PCA 
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import librosa
import gc

# with open('config_trunc15sOf2min.json' , 'r', encoding = 'utf-8-sig') as reader:
with open('config_tagData.json', 'r', encoding='utf-8-sig') as reader:
    config = json.loads(reader.read())

isShowFreqRespon = 0    #config['isShowFreqRespon']
ignoredACCch = config['ignoredACCch']
isOverWriten = config['isOverWriten']
isOnlyacc = config['isOnlyacc']
sDir = config['SrcDir_FA1raw']
Dirs_overW = config['SelectDirs_overw']
ispltacc = 0    #config['plt_acc']
seg_sec = config['seg_sec']
stride_sec = config['stride_sec']
Tend_sec = config['Tend_sec'] if config['Tend_sec'] > 0 else 1e10
Tstart_sec = config['Tstart_sec']
is_even_odd_dstdir = config['even_odd_dstdir']
is_1by1_dstdir = config['1by1_dstdir']
msg_all = ''
msg = ''

def thislog(msg_tmp, mode=None, dirname='.'):
    global msg_all
    msg_all += msg_tmp
    if mode == None:
        print(msg_tmp)
    else:
        print(msg_all, file=open(f'{dirname}/preprocess.log', mode))
        msg_all = ''

def create_dstdir(srcdir, wavfn):
    global seg_sec
    global stride_sec
    global is_even_odd_dstdir
    global is_1by1_dstdir
    DstDir = f'{srcdir}\\trunc\\{os.path.basename(wavfn)[:-4]}-len{seg_sec}_step{stride_sec}'\
                if is_1by1_dstdir else f'{SrcDir}\\trunc'
    if is_even_odd_dstdir:
        DstDir_even = f'{DstDir}\\even'
        if not os.path.exists(DstDir_even):
            os.makedirs(DstDir_even)
        DstDir_odd = f'{DstDir}\\odd'
        if not os.path.exists(DstDir_odd):
            os.makedirs(DstDir_odd)
        return DstDir_even, DstDir_odd
    else:
        if not os.path.exists(DstDir):
            os.makedirs(DstDir)
        return DstDir

#%% ====== filter
sr_acc = 100
nyq = sr_acc/2
N_filt = 3
# === for accSet
wn = np.array([0.05, 1])  # band-pass
# wn = np.array(20) # low-pass        
if np.size(wn)==2:
    filtype = 'bandpass'
    b_butter, a_butter = signal.butter(N_filt, wn/nyq, btype=filtype)
else:
    filtype = 'lowpass'
    b_butter, a_butter = signal.butter(N_filt, wn/nyq, btype=filtype)
# freq response
w_butter, h_butter = signal.freqz(b_butter, a_butter, fs=sr_acc)
if isShowFreqRespon:
    fig_fr = plt.figure(figsize=(10,6))
    ax_fr = fig_fr.subplots(1,1)
    ax_fr_2 = ax_fr.twinx()
    ax_fr.plot(w_butter, 20*np.log10(abs(h_butter)), 'b', label="gain")
    ax_fr_2.plot(w_butter, np.unwrap(np.angle(h_butter,deg=True)), 'r', label="phase")
    ax_fr.grid(axis='both')
    ax_fr.set_xlim((0, 3))
    plt.show()
# # === for acc_PCA
# wn = np.array([0.05, 1])  # band-pass
# # wn = np.array(20) # low-pass        
# if np.size(wn)==2:
#     filtype = 'bandpass'
#     b_butter, a_butter = signal.butter(N_filt, wn/nyq, btype=filtype)
# else:
#     filtype = 'lowpass'
#     b_butter, a_butter = signal.butter(N_filt, wn/nyq, btype=filtype)

# prefix = '2019-04-25-15-16-28'
# a=os.listdir(os.getcwd())
# print(os.getcwd())

if not os.path.exists(sDir) and os.path.exists('G:/我的雲端硬碟/臨床部/[臨床部]-[FA1胸音計畫]'):
    sDir = sDir.replace('G:\\My Drive', 'G:/我的雲端硬碟/臨床部/[臨床部]-[FA1胸音計畫]')
SelectDir = (config['SelectDirs_overw'] if isOverWriten else '')
SrcDirs = []
msg = f'FA1 raw: {sDir}   OverWriten folders:{SelectDir}'
thislog(msg)

# === find FA1 raw data folders to process
for dirP, dirN, fNs in os.walk(sDir):
    rawWavfns = [fn for fn in fNs if (fn.endswith('.wav') or fn.endswith('.WAV')) and not fn.startswith('trunc')]
    if isOverWriten:        # overwrite in SelectDirs
        # print(dirP, len(rawWavfns))
        for tDir in SelectDir:
            if tDir in dirP and len(rawWavfns):
                thislog(f'{dirP} to be overWriten')
                SrcDirs.append(dirP+'\\')
    else:                   # only folders w/o truncated wav files
        # === check if there is any wav file in subfolders
        no_wavfns_subDir = True        
        for folder in dirN:
            no_wavfns_subDir = no_wavfns_subDir and not len([fn for fn in os.listdir(dirP+'/'+ folder) \
                if (fn.endswith('.wav') or fn.endswith('.WAV'))])
            if not no_wavfns_subDir:
                break
        # print(len(rawWavfns), dirP, rawWavfns)
        if len(rawWavfns) and no_wavfns_subDir:     # no 'trunc' in folder name, at least one wav file, no wav file in subfolders
            SrcDirs.append(dirP+'\\')
            msg = f'{dirP} has no truncated files.' 
            thislog(msg)
thislog('', mode='w')
#%%

for SrcDir in SrcDirs:
    # break
    # SrcDir = 'G:\\My Drive\\[臨床部]-[FA1 raw data]\\[FA1]-[臨床]-[20190403]-[FA1聲音欓]\\'
    # SrcDir = 'C:\\Users\\grinl\\downloads\\'
    # rawWavfns = [fn for fn in os.listdir(SrcDir) if fn.endswith(prefix,0,19)]
    timeStamp = time.strftime("%Y%m%d%H%M", time.localtime())
    msg = f'go  {timeStamp} {SrcDir}'
    thislog(msg)

    # ====== truncate wav
    rawWavfns = [fn for fn in os.listdir(SrcDir) if (fn.endswith('.wav') or fn.endswith('.WAV')) and not fn.startswith('trunc')]

    def t2s(t):
        h,m,s = t.strip().split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)

    msg = f'\nlen(files):{len(rawWavfns)}\t{SrcDir}' 
    thislog(msg)
    # print(f'\nlen(files):{len(rawWavfns)}\t{SrcDir}', file=open(f'{SrcDir}preprocess.log', 'a'))
    dict_wavfn_duration = {}

    for fn in rawWavfns:
        if '-[錄音欓]' in SrcDir and not 'mono' in fn:
            msg = f'{fn} is not suitable for this truncation process!\nPlease check its format'
            thislog(msg)
            continue
        wavfn = SrcDir + fn
        if is_even_odd_dstdir:
            DstDir_even, DstDir_odd = create_dstdir(SrcDir, wavfn)
        else:
            DstDir = create_dstdir(SrcDir, wavfn)
        if isOnlyacc:
            break
        msg = f'{rawWavfns.index(fn)}: {fn}'
        thislog(msg)
        # print(f'{rawWavfns.index(fn)}: {fn}', file=open(f'{SrcDir}preprocess.log', 'a'))
        
        # snd, fs = sf.read(tmp)
        try:
            wavdata, sr_wav = librosa.load(wavfn, sr=None)
        except ValueError:
            msg = f'Maybe array is too big'
            thislog(msg)
            # print('Maybe array is too big', file=open(f'{SrcDir}preprocess.log', 'a'))
            continue
        duration_whole = len(wavdata)/sr_wav
        dict_tmp = {fn:duration_whole}
        dict_wavfn_duration.update(dict_tmp)
        msg = f'fs:{sr_wav}  len:{len(wavdata)}(frames) / {duration_whole:.1f}(s)'  
        thislog(msg)
        # if sr_wav != 4000:
        #      wavdata, sr_wav = librosa.load(wavfn, sr=4000)
        # del wavdata
        gc.collect()
        
        # ========= trucate seg_sec every stride_sec
        step = 0
        offset_now = Tstart_sec
        while offset_now < duration_whole - seg_sec and offset_now <= Tend_sec - seg_sec:            
            wavdata, sr_wav = librosa.load(wavfn, sr=None, duration=seg_sec, offset=offset_now)
            truncfn = f'trunc_{os.path.basename(wavfn)[:-4]}_{step:08d}.wav'
            msg = f'\t{step+1}: {offset_now}~{offset_now + seg_sec}/{duration_whole:.1f}sec  output wavfn:{truncfn}'
            thislog(msg)

            if is_even_odd_dstdir:
                if step % 2:
                    sf.write(f'{DstDir_odd}\\{truncfn}', wavdata, sr_wav, subtype='PCM_16')
                else:
                    sf.write(f'{DstDir_even}\\{truncfn}', wavdata, sr_wav, subtype='PCM_16')
            else:
                sf.write(f'{DstDir}\\{truncfn}', wavdata, sr_wav, subtype='PCM_16')
            step += 1
            offset_now += stride_sec
    thislog('', mode='a', dirname=SrcDir)

    # =============== transfer acc data
    key_accfns = []
    # === define keyword list of acc files
    if not os.path.exists(SrcDir+'acc'):    # no ACC data
        continue
    for fn in os.listdir(SrcDir+'acc'):
        if fn.endswith('acc') and not fn[:-5] in key_accfns:
            key_accfns.append(fn[:-5])
    # accfns = [fn[:-5] for fn in os.listdir(SrcDir+'acc') if (fn.endswith('acc') and not fn[:-5] in accfns])]
    for key_fn in key_accfns:
        label_ax = ['x', 'y', 'z']
        for j in range(8): # 8ch
            if j in ignoredACCch:
                continue
            accfn = f'{SrcDir}acc\\{key_fn}{j}.acc'
            wavfn = f'{SrcDir}{key_fn}{j*2}.wav'
            if not os.path.exists(wavfn):
                continue
            msg = f'\naccfn: {accfn}\nwavfn: {wavfn}'
            thislog(msg)
            # continue
            # ================= read all ch
            with open(accfn, 'r', newline='') as csvfile:
                rows = csv.reader(csvfile, delimiter=' ')
                for row in rows:
                    accRaw = row
            # print(f'\t\t debug  {np.array(accRaw[:-1], dtype=np.int)}')
            if np.mean(np.array(accRaw[:-1], dtype=np.int32)) == 0:
                continue
            # sndData = []
            if isOnlyacc:
                # sndData, sr_wav = librosa.load(wavfn, sr=None)
                duration_whole = librosa.get_duration(filename=wavfn)   #len(sndData)/sr_wav
            else:
                duration_whole = dict_wavfn_duration[os.path.basename(wavfn)]

            if len(accRaw) % 3 == 0:
                amount = len(accRaw)/3
            elif len(accRaw) % 3 == 1:
                amount = (len(accRaw)-1)/3
            else:
                amount = (len(accRaw)-2)/3
            msg = f'\nacc> {os.path.basename(accfn)} how many XYZ set:{amount}  duration:{len(accRaw)/sr_acc/3:.1f}(s)'
            msg += f'wav> {os.path.basename(wavfn)} duration:{duration_whole:.1f}' 
            thislog(msg)
            if abs(len(accRaw)/sr_acc/3-duration_whole) > 4:   # skip if the length of acc data doesn't match that of wav
                msg = f'skip becasue the length difference of acc and wav is > 2sec!\nacc:{os.path.basename(accfn)} duration:{len(accRaw)/sr_acc/3:.3f}(s)\nwav:{os.path.basename(wavfn)} duration:{duration_whole:.3f}' 
                # print(f'skip becasue the length difference of acc and wav is > 2sec')
                thislog(msg)
                continue
            # del sndData
            del duration_whole
            print('gc collect',gc.collect())            

            #%% ====== get data from idxi to idxf set
            accSet = []
            idxi = 0  
            idxf = amount   
            for i in range(int(amount)):
                if i < idxf and i > idxi:
                    # accSet.append([accRaw[3*i],accRaw[3*i+1]])
                    accSet.append(accRaw[3*i:3*i+3])
            accSet = np.array(accSet, dtype=np.int32)
            # ================= filtered x,y,z
            accSet_filtered = []
            [accSet_filtered.append(signal.filtfilt(b_butter, a_butter, accSet[:,i])) for i in range(3)]

            #%% ====== fitting data by PCA (n=1) and detrend
            accSet_filtered_trans = np.transpose(accSet_filtered)
            chSels = [[0,1],[0,2],[1,2]]   # ch: x, y, z as input of fitting data
            pca_n1=PCA(n_components=1)
            idx_max = 0
            score_max = 0
            for i in range(len(chSels)):
                newData = pca_n1.fit_transform(accSet_filtered_trans[:,chSels[i]])
                msg = f'\t{i}> ch:{chSels[i]}  score:{pca_n1.explained_variance_ratio_}'
                thislog(msg)
                if pca_n1.explained_variance_ratio_ > score_max:
                    idx_max = i
                    accSet_PCA_n1 = newData
                    variance_max = pca_n1.explained_variance_
                    score_max = pca_n1.explained_variance_ratio_
            chSel = chSels[idx_max]
            msg = f'number of components:{pca_n1.n_components}' 
            msg += f'best match:{chSel}'
            msg += f'The amount of variance:{variance_max}'
            msg += f'The ratio of variance:{score_max}'
            thislog(msg)
            # print(f'acc_PCA_n1>  len:{len(accSet_PCA_n1)}  shape:{np.shape(accSet_PCA_n1)}')
            # print(accSet_PCA)
            # === detrend
            # wn = np.array([0.05, 1])  # band-pass       
            # filtype = 'bandpass'
            # b_butter, a_butter = signal.butter(N_filt, wn/nyq, btype=filtype)
            accSet_PCA_n1_filtered = signal.filtfilt(b_butter, a_butter, accSet_PCA_n1.T)

            #%% ====== fitting data by PCA (n=2)
            pca_n2=PCA(n_components=2)
            accSet_PCA_n2=pca_n2.fit_transform(np.array(accSet_filtered_trans[:,chSel]))
            msg = f'number of components:{pca_n2.n_components}'
            msg += f'The amount of variance:{pca_n2.explained_variance_}'
            msg += f'The ratio of variance:{pca_n2.explained_variance_ratio_}'
            thislog(msg)
            # accSet_PCA_n2_filtered = signal.filtfilt(b_butter, a_butter, accSet_PCA_n2)

            #%% ====== fitting data by PCA (n=auto)
            # pca=PCA(n_components='mle')
            # accSet_PCA_nAuto=pca.fit_transform(np.array(accSet_filtered_trans[:,chSel]))
            # print(f'number of components:{pca.n_components}')
            # print(f'The amount of variance:{pca.explained_variance_}')
            # print(f'The ratio of variance:{pca.explained_variance_ratio_}')

            #%% ====== export accSet, accSet_filtered, accSet_PCA to csv
            accSet_all = np.concatenate((accSet, accSet_filtered_trans, accSet_PCA_n1_filtered.T, accSet_PCA_n2), axis=1)
            # if not os.path.exists(f'{SrcDir}/acc/{os.path.basename(accfn)[:-4]}.csv'):
            with open(f'{SrcDir}{os.path.basename(accfn)[:-4]}.csv','w',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['x_raw','y_raw','z_raw','x_filtered','y_filtered','z_filtered',\
                    f'acc_PCA(n=1)_ratio{float(score_max):.3f}_ch{chSel}',\
                    f'acc_PCA(n=2)_ratio{float(pca_n2.explained_variance_ratio_[0]):.3f}_x',f'acc_PCA(n=2)_ratio{float(pca_n2.explained_variance_ratio_[1]):.3f}_y'])
                [writer.writerow(row) for row in accSet_all]

            # ==== truncate acc data to match truncated WAV
            idx_now = round(Tstart_sec*sr_acc)
            cnt_seg = 1
            buffer_trunc = []
            buffer_trunc_accRaw = []
            while idx_now < len(accSet_all) - seg_sec*sr_acc and idx_now <= (Tend_sec-seg_sec)*sr_acc:
                msg = f'{cnt_seg}: {idx_now}~{idx_now+seg_sec*sr_acc} ({idx_now/sr_acc:.2f}~{(idx_now+seg_sec*sr_acc)/sr_acc:.2f}sec)'
                thislog(msg)
                buffer_trunc.append(accSet_all[idx_now:idx_now+seg_sec*sr_acc])
                buffer_trunc_accRaw.append(accRaw[idx_now*3:(idx_now+seg_sec*sr_acc)*3])
                idx_now += stride_sec*sr_acc
                cnt_seg += 1
            # if idx_row > len(accSet_all)-120*sr_acc and idx_row < len(accSet_all)-15*sr_acc:
            #     print(cnt_seg,'  ', idx_row)
            #     buffer_trunc.append(accSet_all[idx_row:idx_row+15*sr_acc])
            for i in range(len(buffer_trunc)):
                if is_even_odd_dstdir:
                    if i % 2:
                        tmpw = f"{DstDir_odd}\\trunc_{os.path.basename(accfn)[:-4]}_{i}.csv"
                    else:
                        tmpw = f"{DstDir_even}\\trunc_{os.path.basename(accfn)[:-4]}_{i}.csv"
                else:
                    tmpw = f'{SrcDir}trunc/trunc_{os.path.basename(accfn)[:-4]}_{i}.csv'
                if not os.path.exists(f'{SrcDir}trunc'):
                    os.mkdir(f'{SrcDir}trunc')
                msg = f'going to generate truncated acc: {tmpw}' 
                thislog(msg)
                with open(tmpw,'w',newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for row_buffer in buffer_trunc[i]:
                        writer.writerow(row_buffer)

                if is_even_odd_dstdir:
                    if i % 2:
                        tmpw = f"{DstDir_odd}\\trunc_{os.path.basename(accfn)[:-4]}_{i}.acc"
                    else:
                        tmpw = f"{DstDir_even}\\trunc_{os.path.basename(accfn)[:-4]}_{i}.acc"
                else:
                    tmpw = f'{SrcDir}trunc/trunc_{os.path.basename(accfn)[:-4]}_{i}.acc'
                msg = f'going to generate raw truncated acc: {tmpw}'
                thislog(msg)
                with open(tmpw,'w',newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for row_buffer in buffer_trunc_accRaw[i]:
                        writer.writerow(row_buffer)
            thislog('', mode='a', dirname=SrcDir)

            # ================= plot
            if ispltacc:
            #%% range of plot x,y,z of rawdata
                duration = len(accSet[:,0])//sr_acc
                ti = [0, 0, duration//10*9, duration//2]
                tf = [duration, duration//10, duration, duration//2+min(duration//10, 30)]
                for k in range(len(ti)):
                    if duration<ti[k] or duration < tf[k]:
                        ti[k] = duration//2
                        tf[k] = int(ti[k]+40)
                    msg = f'plot>   ti:{ti[k]}  tf:{tf[k]}'
                    thislog(msg, mode='a', dirname=SrcDir)
                    #%% plot x,y,z of rawdata
                    # Timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    fig_accSet = plt.figure(figsize=(16,9))
                    fig_accSet.suptitle(f'{os.path.basename(accfn)}\nraw Data {ti[k]}~{tf[k]}(s)', fontsize=14)
                    ax_acc = fig_accSet.subplots(3,1)        
                    [ax_acc[i].plot(np.arange(0,len(accSet[:,i]))/sr_acc,accSet[:,i], label=label_ax[i]) for i in range(3)]
                    [ax_acc[i].legend(loc=2, fontsize=14) for i in range(3)]
                    [ax_acc[i].set_xlim((ti[k],tf[k])) for i in range(3)]
                    [ax_acc[i].set_ylim((np.min(accSet[:,i][ti[k]*sr_acc:tf[k]*sr_acc]),np.max(accSet[:,i][ti[k]*sr_acc:tf[k]*sr_acc]))) for i in range(3)]
                    [ax_acc[i].set_ylim((np.min(accSet[:,i][ti[k]*sr_acc:tf[k]*sr_acc]),np.max(accSet[:,i][ti[k]*sr_acc:tf[k]*sr_acc]))) for i in range(3)]
                    plt.savefig(f'{SrcDir}acc/{os.path.basename(accfn)[:-4]}_{ti[k]}~{tf[k]}.png')

                    #%% plot x,y,z of filtered data
                    fig_accSet_filtered = plt.figure(figsize=(16,9))
                    ax_acc_filtered = fig_accSet_filtered.subplots(3,1)
                    fig_accSet_filtered.suptitle(f'{os.path.basename(accfn)}\nraw Data {ti[k]}~{tf[k]}(s)', fontsize=14)
                    [ax_acc_filtered[i].plot(np.arange(0,len(accSet_filtered[i]))/sr_acc,accSet_filtered[i], label=label_ax[i]) for i in range(3)]
                    [ax_acc_filtered[i].legend(loc=2, fontsize=14) for i in range(3)]
                    [ax_acc_filtered[i].set_xlim((ti[k],tf[k])) for i in range(3)]
                    [ax_acc_filtered[i].set_ylim((np.min(accSet_filtered[i][ti[k]*sr_acc:tf[k]*sr_acc]),np.max(accSet_filtered[i][ti[k]*sr_acc:tf[k]*sr_acc]))) for i in range(3)]
                    plt.savefig(f'{SrcDir}acc/{os.path.basename(accfn)[:-4]}_{ti[k]}~{tf[k]}_filtered.png')
                    #%%
                    # plt.plot(np.transpose(accSet)[0])
                    # plt.xlim()
                    # plt.show()

                    #%% plot data after PCA
                    accSet_PCA = accSet_PCA_n1
                    fig_accSet_PCA = plt.figure(figsize=(16,9))
                    fig_accSet_PCA.suptitle(f'{os.path.basename(accfn)}\nPCA(n=1)(ch:{chSel}) {ti[k]}~{tf[k]}(s)', fontsize=14)
                    ax_acc_PCA = fig_accSet_PCA.subplots(1,1)
                    ax_acc_PCA.plot(np.arange(ti[k]*sr_acc,tf[k]*sr_acc)/sr_acc, accSet_PCA[ti[k]*sr_acc:tf[k]*sr_acc], label='PCA')
                    ax_acc_PCA.legend(loc=2, fontsize=14)
                    ax_acc_PCA.set_xlim((ti[k],tf[k]))
                    ax_acc_PCA.set_ylim((np.min(accSet_PCA[ti[k]*sr_acc:tf[k]*sr_acc]),np.max(accSet_PCA[ti[k]*sr_acc:tf[k]*sr_acc])))
                    plt.savefig(f'{SrcDir}acc/{os.path.basename(accfn)[:-4]}_{ti[k]}~{tf[k]}_PCA.png')

                    plt.close('all')
                    del accSet_PCA
            del accSet_PCA_n1
            del accRaw
            del accSet            
            del accSet_filtered
            del accSet_all
            del buffer_trunc
            gc.collect()
