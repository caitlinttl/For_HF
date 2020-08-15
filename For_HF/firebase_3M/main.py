# Python bytecode 3.7.3
# pip install pypiwin32
# Auto spectrogram to ppt

import win32com.client
import win32com.client.dynamic
import time
import datetime
import json
import os

print()
print('CHECK "stethoscope-irb-soundinfo-export.json" and "Wavs" are in spectrogram folder !! \n')
datapath = str(input(r'Path of Spectrogram Folder: '))

print()
print('processing...please wait...\n')

startdate = datetime.datetime.now()
t0 = time.perf_counter()

dir = datapath #spectrum folder
NewPPT = dir + '\\Report'
jsonpath = 'C:\\Tzu-Ling\\3M_data_Backup\\stethoscope-irb-soundinfo-export.json'
templatePPT = 'C:\\Tzu-Ling\\pytry\\autoPPT_json\\spectrum_template_json.pptx'

with open(jsonpath, 'r', encoding='utf-8-sig') as reader:
    data3M = json.loads(reader.read())


pngNum = 0
slideNum = 0
noteNum = 0

def PowerPoint(dir):
    global pngNum
    global slideNum
    global noteNum
    allfiles = os.listdir(dir)
    allpng = []
    allwav = []
    allwavName_folder = []
    firstwavname = []
    for file in allfiles:
        if '.png' in os.path.basename(file):
            allpng.append(os.path.join(dir,file))
            firstwavname.append(os.path.splitext(file)[0])
            pngNum += 1
            slideNum = int(pngNum/8)
        if '.wav' in os.path.basename(file):
            allwav.append(os.path.join(dir,file))
            allwavName_folder.append(os.path.basename(file))
    print(f'wav number: {len(allwavName_folder)}\n')
    ppt = templatePPT #temlpate
    App = win32com.client.Dispatch("PowerPoint.Application")
    App.Visible = True
    Presentation = App.Presentations.Open(ppt)  #, WithWindow=False #not open ppt
    # ----- copy n pages of slides p.2
    count = 0
    while count < slideNum:          
        Presentation.Slides(2).Copy() #copy p.2
        Presentation.Slides.Paste(Index=2) #paste in p.2
        count += 1
    # ----- insert No.n(png.1~8) in page.n+1
    wavset = 0   # No.set
    while wavset < slideNum:                          
        pptpage = wavset+2  #No.page
        mySlide = Presentation.Slides(pptpage)
        # ----- filename
        filename = str(firstwavname[8*wavset])
        insertfilename = mySlide.Shapes.Addtextbox(1,750,27,200,300)
        insertfilename.TextFrame.TextRange.Text = filename
        print(filename)    
        # ----- bednumber and metadata
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if filename in str(k3):
                        hardwareInfo = data3M[k1][k2]['hardwareInfo']
                        bedN = str(data3M[k1][k2]['bedNumber'])
                        metaD = str(data3M[k1][k2]['metaData'])
                        print(hardwareInfo)
                        print(bedN)
                        print(metaD + '\n')
                        insertbedN = mySlide.Shapes.Addtextbox(1,750,62,200,300)
                        insertbedN.TextFrame.TextRange.Text = str('Bed number: '+ bedN)
                        insertmetaD = mySlide.Shapes.Addtextbox(1,750,97,200,300)
                        insertmetaD.TextFrame.TextRange.Text = str('Note: \n'+ metaD)
                        noteNum += 1
        # ----- insert png 
        pagespec = 0   # No.png
        for pagespec in range(8*wavset,8*wavset+8): 
            img = str(allpng[pagespec])
            insertspec = mySlide.Shapes.AddPicture(img, LinkToFile=False, SaveWithDocument=True, Left=10, Top=200, Width=100, Height=100)
        # ----- insert wav and preLabel
        wav1 = str(allwav[8*wavset])
        wav1_name = str(allwavName_folder[8*wavset])
        insertWav1 = mySlide.Shapes.AddMediaObject2(wav1, LinkToFile=False, SaveWithDocument=True, Left=395, Top=20, Width=32, Height=32)
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if wav1_name in str(k3):
                        preLabel1 = (data3M[k1][k2]['symptomLabel'])
                        insertpreLabel1 = mySlide.Shapes.Addtextbox(1,158,-4,50,100)
                        insertpreLabel1.TextFrame.TextRange.Text = str(preLabel1)
        wav2 = str(allwav[8*wavset+1])
        wav2_name = str(allwavName_folder[8*wavset+1])
        insertWav2 = mySlide.Shapes.AddMediaObject2(wav2, LinkToFile=False, SaveWithDocument=True, Left=395, Top=155, Width=32, Height=32)
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if wav2_name in str(k3):
                        preLabel2 = (data3M[k1][k2]['symptomLabel'])
                        insertpreLabel2 = mySlide.Shapes.Addtextbox(1,158,129,50,100)
                        insertpreLabel2.TextFrame.TextRange.Text = str(preLabel2)
        wav3 = str(allwav[8*wavset+2])
        wav3_name = str(allwavName_folder[8*wavset+2])
        insertWav3 = mySlide.Shapes.AddMediaObject2(wav3, LinkToFile=False, SaveWithDocument=True, Left=395, Top=290, Width=32, Height=32)
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if wav3_name in str(k3):
                        preLabel3 = (data3M[k1][k2]['symptomLabel'])
                        insertpreLabel3 = mySlide.Shapes.Addtextbox(1,158,262,50,100)
                        insertpreLabel3.TextFrame.TextRange.Text = str(preLabel3)
        wav4 = str(allwav[8*wavset+3])
        wav4_name = str(allwavName_folder[8*wavset+3])
        insertWav4 = mySlide.Shapes.AddMediaObject2(wav4, LinkToFile=False, SaveWithDocument=True, Left=395, Top=425, Width=32, Height=32)
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if wav4_name in str(k3):
                        preLabel4 = (data3M[k1][k2]['symptomLabel'])
                        insertpreLabel4 = mySlide.Shapes.Addtextbox(1,158,396,50,100)
                        insertpreLabel4.TextFrame.TextRange.Text = str(preLabel4)
        wav5 = str(allwav[8*wavset+4])
        wav5_name = str(allwavName_folder[8*wavset+4])
        insertWav5 = mySlide.Shapes.AddMediaObject2(wav5, LinkToFile=False, SaveWithDocument=True, Left=695, Top=20, Width=32, Height=32)
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if wav5_name in str(k3):
                        preLabel5 = (data3M[k1][k2]['symptomLabel'])
                        insertpreLabel5 = mySlide.Shapes.Addtextbox(1,455,-4,50,100)
                        insertpreLabel5.TextFrame.TextRange.Text = str(preLabel5)
        wav6 = str(allwav[8*wavset+5])
        wav6_name = str(allwavName_folder[8*wavset+5])
        insertWav6 = mySlide.Shapes.AddMediaObject2(wav6, LinkToFile=False, SaveWithDocument=True, Left=695, Top=155, Width=32, Height=32)
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if wav6_name in str(k3):
                        preLabel6 = (data3M[k1][k2]['symptomLabel'])
                        insertpreLabel6 = mySlide.Shapes.Addtextbox(1,455,129,50,100)
                        insertpreLabel6.TextFrame.TextRange.Text = str(preLabel6)
        wav7 = str(allwav[8*wavset+6])
        wav7_name = str(allwavName_folder[8*wavset+6])
        insertWav7 = mySlide.Shapes.AddMediaObject2(wav7, LinkToFile=False, SaveWithDocument=True, Left=695, Top=290, Width=32, Height=32)
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if wav7_name in str(k3):
                        preLabel7 = (data3M[k1][k2]['symptomLabel'])
                        insertpreLabel7 = mySlide.Shapes.Addtextbox(1,455,262,50,100)
                        insertpreLabel7.TextFrame.TextRange.Text = str(preLabel7)
        wav8 = str(allwav[8*wavset+7])
        wav8_name = str(allwavName_folder[8*wavset+7])
        insertWav8 = mySlide.Shapes.AddMediaObject2(wav8, LinkToFile=False, SaveWithDocument=True, Left=695, Top=425, Width=32, Height=32)
        for k1 in data3M.keys():
            for k2 in data3M[k1].keys():
                for k3 in data3M[k1][k2].values():
                    if wav8_name in str(k3):
                        preLabel8 = (data3M[k1][k2]['symptomLabel'])
                        insertpreLabel8 = mySlide.Shapes.Addtextbox(1,455,396,50,100)
                        insertpreLabel8.TextFrame.TextRange.Text = str(preLabel8)
        wavset += 1          
    Presentation.SaveAs(NewPPT)


def main():
    PowerPoint(dir)

if __name__ == '__main__':
    main()


enddate = datetime.datetime.now()
t1 = time.perf_counter()
t_delta = t1-t0


print()
print('-------------------------REPORT--------------------------')
print()
print(f'calculating  time: {t_delta:.2f} seconds '+"("+str(enddate-startdate)+")")
print('start        time: '+startdate.strftime('%Y-%m-%d %H:%M:%S %a'))
print('end          time: '+enddate.strftime('%Y-%m-%d %H:%M:%S %a'))
print()
print('png number: ', str(pngNum))
print('set number: ', str(slideNum))
print()
print('CHECK repeat wavname: ', str(int(noteNum - slideNum)))
print()
print('-----------------------END(๑¯∀¯๑)-----------------------')
print()