# from shutil import copyfile
# import os
# import struct

# target_file_path="test.wav"
# working_tmp_file_path="result.wav"

# copyfile(target_file_path, working_tmp_file_path)

# file_state=os.stat(working_tmp_file_path)
# fileLen=file_state.st_size-44
# lenBytes=struct.pack(">I", fileLen)

# f= open(working_tmp_file_path,"rb+")
# f.seek(40)
# f.write(lenBytes)
# f.close()


# from shutil import copyfile
# import os
# import struct

# target_file_path="test.wav"
# working_tmp_file_path="result.wav"

# copyfile(target_file_path, working_tmp_file_path)

# file_state=os.stat(working_tmp_file_path)
# fileLen=file_state.st_size-44
# lenBytes=struct.pack(">I", fileLen)

# f= open(working_tmp_file_path,"rb+")
# f.seek(40)
# f.write(lenBytes)
# f.close()


import shutil
import soundfile as sf
wdir = r'C:\Tzu-Ling\Spectrogram'  # folder of wav
wavfn = 'vocal_repeat.wav' # filename of wav
shutil.copy2(f'{wdir}\\{wavfn}', f'{wdir}\\{wavfn[:-4]}.raw')
y, sr = sf.read(f'{wdir}\\{wavfn[:-4]}.raw', channels=1, samplerate=4000, subtype='FLOAT', endian='LITTLE')
sf.write(f'{wdir}\\{wavfn}', y, sr, 'PCM_24')