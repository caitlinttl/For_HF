import xlrd         #使用excel read的lib

group = ['G01_PDM_MC_C','G02_PDM_MC_TT','G03_PDM_OV_C','G04_PDM_OV_TT']        #檔案名稱
ROI = ['1','2','3','4','5','6','7','8']
behavior = ['01_PCS','02_STAIs','03_STAIt','04_BAI','05_BDI','06_MPQ']
excel = ['1','2']

for g in group:
        for r in ROI:
                for b in behavior:
                    for e in excel:
                        result="D:/LargeD/zCplandata/Cplan_2017/For_IRB_69/correlation/"+g+"/ROI"+r+"/"+b+"/spm_2019Feb27_00"+e+".xls"     #檔案名稱
                        myWorkbook = xlrd.open_workbook(result) #連結檔案
                        mySheets = myWorkbook.sheets()    #獲取sheet內容
                        mySheet = mySheets[0]     #第一頁sheet
                        nrows = mySheet.nrows     #查有幾列
                        for j in range(nrows):     #查每一列的值
                                if j > 2:           #前兩列不要看
                                    myCell = mySheet.cell(j, 2)   #查第一列C欄位的值
                                    myCellValue  = myCell.value   #將值取出
                                    if myCellValue != '':           #不等於空白才看
                                        if myCellValue < 0.05:     #如果裡面有值小於0.05的回報說是哪份檔案
                                            print(result)
                                            break    #只要有小於0.05的report完就離開loop
