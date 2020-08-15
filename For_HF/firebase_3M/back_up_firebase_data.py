import os
import logging
import datetime
import shutil
from os.path import join, getsize
import time
from selenium import webdriver

firebaseID = 'yilin.wu@heroic-faith.com'
firebasePassword = 'erin920501'
chromedriverPath = r'C:\Tzu-Ling\3M_data_Backup\chromedriver.exe'
jsonSrc = r'C:\Users\Administrator\Downloads\stethoscope-irb-soundinfo-export.json'
josnDst = r'C:\Tzu-Ling\3M_data_Backup\stethoscope-irb-soundinfo-export.json'


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, filename='C:\\Tzu-Ling\\3M_data_Backup\\backup_record.log', filemode='a', format=FORMAT, datefmt=DATE_FORMAT)


t0 = datetime.datetime.now()
logging.info('start update json file')

try: 
    browser = webdriver.Chrome(chromedriverPath)    
    browser.get("https://console.firebase.google.com/u/0/project/stethoscope-irb/database/stethoscope-irb/data/soundinfo")
    browser.find_element_by_id('identifierId').send_keys(firebaseID)
    time.sleep(2)
    browser.find_element_by_id('identifierNext').click()
    time.sleep(10)
    browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(firebasePassword)
    time.sleep(2)
    browser.find_element_by_id('passwordNext').click()
    time.sleep(14)
    browser.find_element_by_xpath('//*[@id="main"]/fire-router-outlet/ng-component/ngh-database-data/div/div/div/div/multi-database-card/fb-multi-resource-card/fb-master-detail-card/md-single-grid/md-card/div/ng-transclude[2]/fb-detail/fb-multi-resource-detail/div/multi-database-body/database-data-viewer/md-single-grid/md-card/interactive-url/nav/div/md-menu').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="menu_container_8"]/md-menu-content/md-menu-item[1]').click()
    time.sleep(20)
    browser.quit()
    # browser.close()
    shutil.move(jsonSrc, josnDst)
    logging.info('complete update json file.')
except Exception as e:
    logging.info(e)
    logging.info('Json file NO update!!!')



t1 = datetime.datetime.now()
logging.info('start download from firebase.')

os.system('gsutil -m cp -r dir gs://stethoscope-irb.appspot.com/sounds/irb/3m C:/Tzu-Ling/3M_data_Backup/back_update')
logging.info('complete download from firebase.')

t2 = datetime.datetime.now()
t_delta_t2_t1 = str(t2-t1)
logging.info("download elapsed time: "+t_delta_t2_t1[0:7])

size = 0
fileList = [] 
for root, dirs, files in os.walk('C:\\Tzu-Ling\\3M_data_Backup\\back_update\\'):
    # size += sum([getsize(join(root, name)) for name in files])
    for name in files:
        f = join(root, name)
        size += getsize(f)
        fileList.append(f)

        
# print(size)


try:
    logging.info('start copy to GD.')
    shutil.copytree('C:\\Tzu-Ling\\3M_data_Backup\\back_update','G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[3M_data_Backup]\\auto_backup')
    logging.info('complete copy to GD. (by shutil)')
except FileExistsError:
    # logging.info('start remove old folder.')
    # shutil.rmtree('G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[3M_data_Backup]\\auto_backup')
    # while os.path.exists('G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[3M_data_Backup]\\auto_backup'):
    #     logging.info('Deletion incomplete. sleep 5 seconds.') 
    #     time.sleep(5) 
    # else:
    #     logging.info('complete remove old folder.')
    #     logging.info('start copy to GD.')
    #     shutil.copytree('C:\\Tzu-Ling\\3M_data_Backup\\back_update','G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[3M_data_Backup]\\auto_backup')
    #     logging.info('complete copy to GD.')
    os.system('Xcopy C:\\Tzu-Ling\\3M_data_Backup\\back_update "G:\\我的雲端硬碟\\臨床部\\[臨床部]-[FA1胸音計畫]\\[胸音計劃]-[聲音分析]\\[音訊] -[資料庫與院內收集]\\[臨床部]-[3M_data_Backup]\\auto_backup" /E /Y')
    logging.info('complete copy to GD. (by system copy)')

t3 = datetime.datetime.now()
t_delta_t3_t2 = str(t3-t2)
logging.info("copy elapsed time: "+t_delta_t3_t2[0:7])

t_delta_t3_t0 = str(t3-t0)
logging.info("total elapsed time: "+t_delta_t3_t0[0:7])

logging.info(f'total: {(size/1024/1024/1024):.3f} GB')
logging.info(f'total: {len(fileList)} wavs\n')


