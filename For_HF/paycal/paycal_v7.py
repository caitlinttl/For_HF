# Python bytecode 3.7.3 
# pip install pywin32

import datetime
import time
import os

import win32com.client
import win32com.client.dynamic
from win32com.client import constants

print()
datapath = str(input(r'請輸入檔案資料夾路徑: '))

print()
# wavtype = str(input('請輸入要計算 胸音(l) or 喉音(t) ? '))

# print()


# startdate = datetime.datetime.now()
finishtime = str(input("finishtime? "))


def countFileLines(filename):
    count=0
    handle = open(filename,'rb')
    for line in handle:
        count+=1
    return count

txtNum = 0
wavNum = 0
 
def listdir(dir,lines):
    global txtNum
    global wavNum
    global labeler
    global labelername
    global laberN
    global laberA
    global folderN
    files = os.listdir(dir)  #列出目錄下的所有文件和目錄
    for file in files:
        filepath = os.path.join(dir,file)
        if os.path.isdir(filepath):  #如果filepath是目錄，遞歸遍歷子目錄
           listdir(filepath,lines)
        elif os.path:   #如果filepath是文件，直接統計行數
            if os.path.splitext(file)[1]=='.txt' :
                txtNum = txtNum+1
                # lines.append(countFileLines(filepath))
                # print(file + ':'+str(countFileLines(filepath)))
                for labeltxt in os.path.splitext(file)[0]:
                    if 'crystal11300' in  os.path.splitext(file)[0]:
                        labeler = '蔡宛玲(crystal11300)'
                        labelername = '宛玲'
                        laberN = '蔡宛玲'
                        laberA = 'crystal11300'
                        folderN = '(crystal)'
                    if 'snoopy19890119' in os.path.splitext(file)[0]:
                        labeler = '林念蓁(snoopy19890119)'
                        labelername = '念蓁'
                        laberN = '林念蓁'
                        laberA = 'snoopy19890119'
                        folderN = '(snoopy)'
                    if 'cindy21562156' in os.path.splitext(file)[0]:
                        labeler = '游昱純(cindy21562156)'
                        labelername = '昱純'
                        laberN = '游昱純'
                        laberA = 'cindy21562156'
                        folderN = '(cindy)'
                    if 'suewcity' in os.path.splitext(file)[0]:
                        labeler = '許舒沛(suewcity)'
                        labelername = '舒沛'
                        laberN = '許舒沛'
                        laberA = 'suewcity'
                        folderN = '(suewcity)'
            if os.path.splitext(file)[1]=='.wav' :
                wavNum = wavNum+1


def DOCX(dir):
    word = win32com.client.gencache.EnsureDispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = False
    doc = word.Documents.Add()
    # mydocx = templateDOCX
    # doc = word.Documents.Open(mydocx)
    range1 = doc.Range(0,0)
    range1.InsertAfter('標註人員: ' + laberN + '\n')
    range1.InsertAfter('標註帳號: ' + laberA + '\n\n')
    paras = doc.Paragraphs
    rangeN = paras(1).Range
    rangeN.Font.Color = 0xFF4b2b
    rangeN.Font.Bold = 1
    rangeA = paras(2).Range
    rangeA.Font.Color = 0xFF4b2b
    rangeA.Font.Bold = 1
    # if wavtype == '胸音' or wavtype == 'l':
    #     range1.InsertAfter(startdate.strftime('%Y%m%d ') + '共' + str(lung) + '元\n\n\n' )
    # if wavtype == '喉音' or wavtype == 't':
    #     range1.InsertAfter(startdate.strftime('%Y%m%d ') + '共' + str(trachra) + '元\n\n\n' )
    range1.InsertAfter(finishtime + '共 3000 元\n\n\n' )
    rangeT = paras(4).Range
    rangeT.Font.Color = 0x0000FF
    rangeT.Font.Bold = 1
    rangeT.Font.Underline = 1
    # range1.InsertAfter('(家中標註)計算原則:\n1個音檔3元，每增加1個標註多0.6元\nEX:100個音檔，共600個標註，即 100*3 + 600*0.6 =660 元  \n(喉音之未能標註音檔不列入計算)(若金額非整數則四捨五入)\n\n\n')
    range1.InsertAfter('(家中標註)計算原則:\n1包固定為3000元\n胸音或小兒喉音1包有250~350個音檔\n成人喉音1包有450~550個音檔\n\n\n')
    range1.InsertAfter('---------------Calculation Details---------------\n')
    range1.InsertAfter('標註人員: '+labeler + '\n')
    # range1.InsertAfter('時間: '+startdate.strftime('%Y-%m-%d %H:%M:%S %a')+ '\n')
    range1.InsertAfter('完成時間: '+finishtime + '\n')
    range1.InsertAfter('檔案路徑: '+dir + '\n\n')
    range1.InsertAfter('音檔(wav)數量: '+str(wavNum) + '\n')
    range1.InsertAfter('標註檔案(txt)數量: '+str(txtNum) + '\n')
    # range1.InsertAfter('標註(label)數量: '+str(sum(lines)) + '\n')
    # if wavtype == '胸音' or wavtype == 'l':
    #     range1.InsertAfter('一般胸音標註費用計算: ' +'('+str(wavNum) +')' +'*3元' + ' + ' +'('+str(sum(lines)) +')'+'*0.6元' +' = ' +str(wavNum*3) +' + ' +str(sum(lines)*0.6)  +' = ' +str(lung) +'元' + '\n')
    # if wavtype == '喉音' or wavtype == 't':
    #     range1.InsertAfter('喉音標註費用計算: '  +'('+str(txtNum) +')' +'*3元' + ' + ' +'('+str(sum(lines)) +')'+'*0.6元' +' = ' +str(txtNum*3) +' + ' +str(sum(lines)*0.6)  +' = ' +str(trachra) +'元' + '\n')
    range1.InsertAfter('1包音檔費用固定為: 3000元\n')
    range1.InsertAfter('---------------------------End---------------------------')
    if os.path.exists (checkre):
        print('repeat')
        word.DisplayAlerts = False
        doc.SaveAs(reNewDOCX)
        doc.SaveAs(reNewPDF, FileFormat=17)
    else:
        word.DisplayAlerts = False
        doc.SaveAs(newDOCX)
        doc.SaveAs(newPDF, FileFormat=17)
    doc.Close()
    word.Quit()


def XLSX(dir):
    excel = win32com.client.Dispatch('Excel.Application')
    excel.Visible = False
    excel.DisplayAlerts = False
    myxlBook = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\statistic.xlsx'
    xlBook = excel.Workbooks.Open(myxlBook)
    xlSheet_this_month = xlBook.Worksheets('當月')
    xlSheet_all = xlBook.Worksheets('all')
    countrow = 0
    allcountrow = 0
    if laberA == "snoopy19890119":
        whichCol = 1
    if laberA == "crystal11300":
        whichCol = 3
    if laberA == "cindy21562156":
        whichCol = 5
    if laberA == "suewcity":
        whichCol = 7
    for i in range(1,60000):
        content = xlSheet_this_month.cells(i,whichCol).value
        if content is not None:
            countrow += 1
        else: 
            break
    for j in range(1,60000):
        contentall = xlSheet_all.cells(j,whichCol).value
        if contentall is not None:
            allcountrow += 1
        else: 
            break
    # xlSheet_this_month.Cells(countrow+1,whichCol).Value = startdate.strftime('%Y%m%d')
    # xlSheet_all.cells(allcountrow+1,whichCol).Value = startdate.strftime('%Y%m%d')
    xlSheet_this_month.Cells(countrow+1,whichCol).Value = finishtime
    xlSheet_all.cells(allcountrow+1,whichCol).Value = finishtime
    xlSheet_this_month.Cells(countrow+1,whichCol+1).Value = "3000"
    xlSheet_all.cells(allcountrow+1,whichCol+1).Value = "3000"
    # if wavtype == '胸音' or wavtype == 'l':
    #     xlSheet_this_month.Cells(countrow+1,whichCol+1).Value = lung
    #     xlSheet_all.cells(allcountrow+1,whichCol+1).Value = lung
    # if wavtype == '喉音' or wavtype == 't':
    #     xlSheet_this_month.Cells(countrow+1,whichCol+1).Value = trachra
    #     xlSheet_all.cells(allcountrow+1,whichCol+1).Value = trachra
    xlBook.Save()
    xlBook.Close()
    # excel.Quit() # exit app
            

lines = []
# dir = 'G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[已標註聲音]\\[已標註]-[3M data]\\20191113-all (9)3M_normal'
dir = datapath
listdir(dir,lines)

# trachra = round(txtNum*3 + sum(lines)*0.6)
# lung = round(wavNum*3 + sum(lines)*0.6)
trachra = lung = 3000

# templateDOCX = 'D:\\LargeD\\Python_py\\paycal\\(範本)20200102 念蓁標註總帳.docx'
# newDOCX = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\doc\\'  + startdate.strftime('%Y%m%d ') + labelername + '標註總帳'
# newPDF = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\'  + startdate.strftime('%Y%m%d ') + labelername + '標註總帳'

# checkre = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\'  + startdate.strftime('%Y%m%d ') + labelername + '標註總帳.pdf'

# reNewDOCX = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\doc\\'  + startdate.strftime('%Y%m%d')+ '_1 ' + labelername + '標註總帳'
# reNewPDF = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\'  + startdate.strftime('%Y%m%d') + '_1 '+ labelername + '標註總帳'

newDOCX = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\doc\\'  + finishtime + labelername + '標註總帳'
newPDF = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\'  + finishtime + labelername + '標註總帳'

checkre = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\'  + finishtime + labelername + '標註總帳.pdf'

reNewDOCX = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\doc\\'  + finishtime+ '_1 ' + labelername + '標註總帳'
reNewPDF = 'G:\\我的雲端硬碟\\[聿信醫療]_呼吸音標註外包\\a_PayCal\\標註記錄'+ folderN + '\\'  + finishtime + '_1 '+ labelername + '標註總帳'


DOCX(dir)
XLSX(dir)



print(' ')
print('-------------TIME and DATA------------')
print(' ')
print('標註人員: '+labeler)
print()
# print('時間: '+startdate.strftime('%Y-%m-%d %H:%M:%S %a'))
print('完成時間: '+ finishtime)
print(' ')
print('檔案路徑: '+dir)
print(' ')
print('----------------REPORT----------------')
print(' ')
print('音檔(wav)數量: '+str(wavNum))
print('標註檔案(txt)數量: '+str(txtNum))
# print('標註(label)數量: '+str(sum(lines)))

print("1包音檔費用固定為: 3000元")

# if wavtype == '胸音' or wavtype == 'l':
#     print('一般胸音標註費用計算: ' +'('+str(wavNum) +')' +'*3元' + ' + ' +'('+str(sum(lines)) +')'+'*0.6元' +' = ' +str(wavNum*3) +' + ' +str(sum(lines)*0.6)  +' = ' +str(lung) +'元')
# if wavtype == '喉音' or wavtype == 't':
#     print('喉音標註費用計算: '  +'('+str(txtNum) +')' +'*3元' + ' + ' +'('+str(sum(lines)) +')'+'*0.6元' +' = ' +str(txtNum*3) +' + ' +str(sum(lines)*0.6)  +' = ' +str(trachra) +'元')

print(' ')
print('-----------------END------------------')
print(' ')








