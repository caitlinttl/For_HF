import csv
import json

csvFilepath = "for_main_json.csv"
jsonFilepath = "ALL_mainJson.json"


#----- Read the CSV and add the data to a dictionary
data = {}
with open(csvFilepath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for csvRow in csvReader:
        clipUUID = csvRow["clipUUID"]
        data[clipUUID] = csvRow
    # print(data)

#----- Write all data to a JSON file
with open(jsonFilepath, "w",encoding='utf-8') as jsonFile:
    jsonFile.write(json.dumps(data, ensure_ascii=False, indent=4))  # chinese and json format

#----- Write each data to each JSON file
allWavName = []
allClipUUID = []
with open(jsonFilepath, "r", encoding='utf-8') as jsonFile:
    wavinfodata = json.loads(jsonFile.read())
    allwavNum = len(wavinfodata.keys())
    print('totel wav number: '+ str(allwavNum))
    for k1 in wavinfodata.keys():
        allClipUUID.append(k1)
        WavName = wavinfodata[k1]["fileName"]
        allWavName.append(str(WavName))
    print(allClipUUID)
    print(allWavName)
    count = 0
    while count < allwavNum:
        onedata = wavinfodata[allClipUUID[count]]
        print(onedata)
        if onedata["fileName"] == "音檔名":
            jsonFilepath_each = str("translation_main.json")
        else: 
            jsonFilepath_each = str(allWavName[count])[:-4] + "_main.json"
        print(jsonFilepath_each)
        with open(jsonFilepath_each, "w",encoding='utf-8') as jsonFileSub:
            jsonFileSub.write(json.dumps(onedata, ensure_ascii=False, indent=4))
        count += 1

