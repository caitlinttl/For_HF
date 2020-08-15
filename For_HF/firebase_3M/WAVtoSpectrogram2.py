#%%
# =============== WAV list to spectrogram

import matplotlib.pyplot as plt
# import soundfile as sf
import numpy as np
import os
import csv
import librosa, librosa.display
import json
# import subprocess
import time
# import matplotlib.image as matimg
# from shutil import copyfile
# from PIL import Image
import matplotlib
chinese_font = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\mingliu.ttc')

import utils as utils
#%%
with open('config_tagData.json', 'r', encoding='utf-8-sig') as reader:
    config = json.loads(reader.read())


srcDIRs = config['srcDIRs_wav2specgram']
scr_dim = config['scr_dim_wav2specgram']
ti = time.perf_counter()
for idx,SrcDir in enumerate(srcDIRs):
    print(f'{idx}:\nCurrent Dir:{SrcDir}')
    suffix = 'wav'
    sndfn = [fn for fn in os.listdir(SrcDir) if fn.endswith(suffix)]
    
    DstDir = f'{SrcDir}/Spectrogram/'
    print(f'DstDir:{DstDir}')
    if not os.path.exists(DstDir):
        os.makedirs(DstDir)

    # ======  wav to spectrogram
    wavfns = [f'{SrcDir}\\{fn}' for fn in os.listdir(SrcDir) if fn.endswith('wav')]
    wavfn_cnt = len(wavfns) if config['plot_all_in_one'] else 1
    for i, wavfn in enumerate(wavfns):
        print(wavfn)
        # snd, sr = sf.read(wavfn)
        snd, sr = librosa.load(wavfn, sr=None)
        if snd.ndim == 2:  # ignore one of dual channel
            snd = snd[:,0]
        if sr != 4000:
            snd, sr = librosa.load(wavfn, sr=4000)
        duration = len(snd)/sr
        fftlen = 512
        hop = round(fftlen*.75)
        pad_to = round(fftlen*1.5)
        if wavfn_cnt == 1:
            imgfn = f'{DstDir}\\{os.path.basename(wavfn)[:-4]}.png'
            fig, ax = plt.subplots(1, 1, figsize=(scr_dim[0]/100,scr_dim[1]/100), clear=True)
            Sxx, f, t, im = ax.specgram(snd, NFFT=fftlen, Fs=sr, noverlap=hop, pad_to=pad_to, 
                                        cmap='afmhot',vmin=-105,vmax=-15)
            stft_x_len_per_sec = Sxx.shape[1]/duration
            stft_y_len_per_Hz = Sxx.shape[0]/2000
            intensity_wav = utils.getWavIntensity(snd[:int(15*sr)], sr, duration)
            t_envelope_sec, envelope, sr_envelope \
                = utils.getEnvelopWAV(Sxx, duration, sr,
                                intensity_wav,
                                stft_x_len_per_sec, stft_y_len_per_Hz,
                                time_len_sec=duration/150, time_stride_sec=min(.4, duration/750),
                                freqband_node_Hz=[90,700],
                                freqband_weight=[1])
            ax.plot(t_envelope_sec, envelope/envelope.max()*1500, 'c')
            fn_short = '\\'.join(wavfn.split('\\')[2:-1])
            plt.suptitle(f"{fn_short}\n{os.path.basename(wavfn)}",
                        fontproperties=chinese_font, fontsize=13)
            plt.tight_layout(rect=(0.0, 0.0, 1, 0.94))
            if duration > 30:
                plt.xticks(np.arange(0,t[-1]+1,round(duration/29)))
            else:
                plt.xticks(np.arange(0,t[-1]+1,1))
            plt.yticks(np.arange(0,f[-1]+100,100))
            plt.ylim((0,1800))
            plt.savefig(imgfn)
        else:
            if i == 0:
                imgfn = f'{DstDir}{os.path.basename(SrcDir)}.png'
                fig, ax = plt.subplots(wavfn_cnt, 1, figsize=(scr_dim[0]/100,scr_dim[1]*wavfn_cnt*0.9/100), clear=True)
            Sxx, f, t, im = ax[i].specgram(snd, NFFT=fftlen, Fs=sr, noverlap=hop, pad_to=pad_to, 
                                        cmap='afmhot',vmin=-105,vmax=-15)
            stft_x_len_per_sec = Sxx.shape[1]/duration
            stft_y_len_per_Hz = Sxx.shape[0]/2000
            intensity_wav = utils.getWavIntensity(snd[:int(15*sr)], sr, duration)
            t_envelope_sec, envelope, sr_envelope \
                = utils.getEnvelopWAV(Sxx, duration, sr,
                                intensity_wav,
                                stft_x_len_per_sec, stft_y_len_per_Hz,
                                time_len_sec=duration/150, time_stride_sec=min(.4, duration/750),
                                freqband_node_Hz=[90,700],
                                freqband_weight=[1])
            ax[i].plot(t_envelope_sec, envelope/envelope.max()*1500, 'c')
            fn_short = '\\'.join(wavfn.split('\\')[2:-1])
            ax[i].set_title(f"{fn_short}\{os.path.basename(wavfn)}",
                            fontproperties=chinese_font, fontsize=13)
            if duration > 30:
                ax[i].set_xticks(np.arange(0,t[-1]+1,round(duration/29)))
            else:
                ax[i].set_xticks(np.arange(0,t[-1]+1,1))
            ax[i].set_yticks(np.arange(0,f[-1]+100,100))
            ax[i].set_ylim((0,1800))
            if i == wavfn_cnt -1:
                plt.tight_layout(rect=(0.0, 0.0, 1, 0.98))
                plt.savefig(imgfn)
tf = time.perf_counter()
print(f'elapsed time: {tf-ti:.3f}')
    
    

#%%
