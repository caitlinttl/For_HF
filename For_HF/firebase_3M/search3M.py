# python 3.7.3 64-bit
# issue: same time and same user >> should search hardwareID

import os
import shutil
import json
import time

isDownload = 1

searchStart = 20191001
searchEnd = 20200511

username = "" # all user
prelabel = "" # all prelabel
recordPosition = "" # all position

username = "H30sn9PBu8MEuEOCKBxznFu3Uqh2" # sara
# username = "YewQB9JoAfW8iK9XnmOeibYKp5b2" # jessica
# username = "ogTgklZh9JSW3dpd9dpfyBUrTI73" # TMU
# username = "20Q8224FjuO7XEY1SbXA8fwDXYT2" # miki
# username = "4eUoLNmNLeRuuBMNXWfPsFYBAOh2" # r.elephant
# username = "3QPuEvVpYqgHGHc1H5syeEPcJBB2" # snoopy
# username = "CpFu3FxyK0MYqAHkUBBW1aOgf973" # crystal
# username = "AmSavNYVRTaFs8shakfoKcUeFLA3" # clhuang1015
# username = "O0lr75R8AXV8b9xrFbqFb8pYnJs2" # carina.cheng
# username = "xreYxXH8YsWFABicLC1QhShuqJB2" # suewcity
# username = "xwGOqUaxbfX5pPYfmRjXCK1jyax2" # lanne.chen@hsiaohospital.org

prelabel = "Wheeze"
# prelabel = "Rale"
# prelabel = "Rhonchi"
# prelabel = "Normal"

# recordPosition = "R_midclevicular_line_and_Rib_2_3"
# recordPosition = "R_midclevicular_line_and_Rib_6_7"
# recordPosition = "R_midaxillary_line_and_Rib_4_5"
# recordPosition = "R_midaxillary_line_and_Rib_10"
# recordPosition = "L_midclevicular_line_and_Rib_2_3"
# recordPosition = "L_midclevicular_line_and_Rib_6_7"
# recordPosition = "L_midaxillary_line_and_Rib_4_5"
# recordPosition = "L_midaxillary_line_and_Rib_10"

outputdir = "C:\\Tzu-Ling\\pytry\\search_3M_data\\output\\"
filepath3M = "C:\\Tzu-Ling\\3M_data_Backup\\back_update\\"
jsonpath = "C:\\Tzu-Ling\\3M_data_Backup\\stethoscope-irb-soundinfo-export.json"

t0 = time.perf_counter()

copyfile = []
copyfile2_caseuuid = []
bedNumberall = []
with open(jsonpath, 'r', encoding='utf-8-sig') as reader:
    data3M = json.loads(reader.read())
    for k1 in data3M.keys():
        for k2 in data3M[k1].keys():
            content = []
            for k3 in data3M[k1][k2].values():
                content.append(str(k3))
            content_str = ",".join(content)
            # print(content_str)
            if username in content_str and prelabel in content_str and recordPosition in content_str:
                fileName = data3M[k1][k2]['fileName']
                caseUUID = data3M[k1][k2]['caseUUID']
                bedNumber = data3M[k1][k2]['bedNumber']
                filetime = fileName[6:14]
                if int(filetime) >= searchStart and int(filetime) <= searchEnd:
                    copyfile.append(fileName)
                    copyfile2_caseuuid.append(caseUUID)
                    bedNumberall.append(bedNumber)

print(copyfile)  
copyfile2_caseuuid_set = set(copyfile2_caseuuid) 
print(copyfile2_caseuuid_set) 
print(bedNumberall)
print(len(bedNumberall))

allcase = []
a = 0
while a < len(bedNumberall):
    allcase.append(bedNumberall[a])
    a += 8

print(f"all norepeat: {set(bedNumberall)}\n")       
print(f"all case: {allcase}")        
print("search wavs: "+str(len(copyfile)))
print("case numbers: "+str(len(copyfile2_caseuuid_set))+"\n")


download_byfilename = []
download_byUUID = []
for root, dirs, files in os.walk(filepath3M):
    for name in files:
        allwav = str(os.path.join(root, name))
        for copywav in copyfile:
            if copywav in allwav:
                # print(allwav)
                download_byfilename.append(allwav)
        for copywav_uuid in copyfile2_caseuuid_set:
            if copywav_uuid in allwav:
                download_byUUID.append(allwav)

print("download wavs_filename: "+str(len(download_byfilename)))
print("download wavs_uuid: "+str(len(download_byUUID)))

if isDownload == 1:
    if username == "" or prelabel != "" or recordPosition != "":
        print("Download by filename.")
        for d1 in download_byfilename:
            shutil.copy(d1,outputdir+d1[-27:])
    else:
        print("Just search user. Download by UUID.")
        for d2 in download_byUUID:
            shutil.copy(d2,outputdir+d2[-27:])
else: print(f'No download!')


t1 = time.perf_counter()
t_delta = t1-t0
print(f"elapsed time: {t_delta:.2f} seconds")