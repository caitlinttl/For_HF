from shutil import copyfile
import os
import struct

input_dir_path='./input'
output_dir_path='./output'


in_file_names = os.listdir(input_dir_path)
print(in_file_names)


if(not os.path.exists(output_dir_path)):
    os.makedirs(output_dir_path)


for fn in in_file_names:
    
    target_file_path=input_dir_path+'/'+fn
    working_tmp_file_path=output_dir_path+'/'+fn

    copyfile(target_file_path, working_tmp_file_path)

    file_state=os.stat(working_tmp_file_path)
    fileLen=file_state.st_size-44
    lenBytes=struct.pack(">I", fileLen)

    f= open(working_tmp_file_path,"rb+")
    f.seek(40)
    f.write(lenBytes)
    f.close()

