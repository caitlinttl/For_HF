from shutil import copyfile
import os
import struct

target_file_path="test.wav"
working_tmp_file_path="result.wav"

copyfile(target_file_path, working_tmp_file_path)

file_state=os.stat(working_tmp_file_path)
fileLen=file_state.st_size-44
lenBytes=struct.pack(">I", fileLen)

f= open(working_tmp_file_path,"rb+")
f.seek(40)
f.write(lenBytes)
f.close()