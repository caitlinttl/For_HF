import os
import json

filepath3M = "C:\\Tzu-Ling\\pytry\\forSH\\KDD_dataset_v2"
jsonpath = "C:\\Tzu-Ling\\pytry\\forSH\\stethoscope-irb-soundinfo-export.json"

wavs = []
for root, dir, files in os.walk(filepath3M):
    for allfile in files:
        if '.wav' in allfile:
            if 'steth_' in allfile:
                # print(allfile)
                wavs.append(allfile)
print(len(wavs))

caseUUID_need = []
with open(jsonpath, 'r', encoding='utf-8-sig') as reader:
    data3M = json.loads(reader.read())
    for k1 in data3M.keys():
        for k2 in data3M[k1].keys():
            for k3 in data3M[k1][k2].values():
                for wav in wavs:
                    if wav in str(k3):
                        caseUUID = data3M[k1][k2]['caseUUID']
                        caseUUID_need.append(caseUUID)
                        # print(caseUUID)
# print(caseUUID_need)
caseUUID_need_set = set(caseUUID_need)
answer = len(caseUUID_need_set)
print(caseUUID_need_set)
print(answer)


