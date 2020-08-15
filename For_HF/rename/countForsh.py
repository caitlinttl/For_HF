import os
import json

filepath3M = "C:\\Tzu-Ling\\pytry\\forSH\\KDD2020_HealthDay\\3M"
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
bedNumber_need = []
with open(jsonpath, 'r', encoding='utf-8-sig') as reader:
    data3M = json.loads(reader.read())
    for k1 in data3M.keys():
        for k2 in data3M[k1].keys():
            for k3 in data3M[k1][k2].values():
                for wav in wavs:
                    if wav in str(k3):
                        caseUUID = data3M[k1][k2]['caseUUID']
                        bedNumber = data3M[k1][k2]['bedNumber']
                        caseUUID_need.append(caseUUID)
                        bedNumber_need.append(bedNumber)
                        # print(caseUUID)
                        print(bedNumber)
# print(caseUUID_need)
caseUUID_need_set = set(caseUUID_need)
bedNumber_need_set = set(bedNumber_need)
bedNumber_need_noSpace = list(filter(None, bedNumber_need))
answer = len(caseUUID_need_set)
answer2 = len(bedNumber_need_set)
answer3 = len(bedNumber_need_noSpace)

print(caseUUID_need_set)
print(answer)

print(bedNumber_need_noSpace)
print(answer3)

print(f'all case (no repeat): {bedNumber_need_set}')
print(f'all case number (no repeat): {answer2}')


