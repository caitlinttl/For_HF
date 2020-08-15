import os

path = r'C:\Tzu-Ling\sw-wav-to-mp3-comparator-master\dst-wav'

for roots, dirs, files in os.walk(path):
    for afile in files:
        afileName = str(afile)  
        fileName = str(os.path.join(roots, afile)) 
        NewFileName = fileName.replace("src","鏡檢_淺慢_成人_type3")
        os.rename(fileName, NewFileName)



