import datetime
import re
import pytz
import time

tz = pytz.timezone('Asia/Hong_Kong')
bj = datetime.datetime.now(tz)

dates = []
for i in range(0 - bj.weekday(), 9 - bj.weekday()):
    dates.append(bj + datetime.timedelta(days=i))
weekdays = []
for x in range(7):
    weekdays.append(dates[x].strftime("%Y/%m/%d"))
print("本周日期：", weekdays)

BaseDKP = 15


def cvl(line):
    # 删除消耗
    step1 = re.sub("\s*\d+\s*\d+\s*\d+\s*$", "", line)
    # 删除帮众名空白至帮派间空白()包括职位
    step2 = re.sub("\s*(龙首|长老|副龙首|无职位|特需官)\s*", "\t", step1)
    return step2


def event2dkp(num):
    defaultrw = 0
    # 委任
    if num.wr > 21:
        defaultrw += 3 * BaseDKP
    else:
        defaultrw += (num.wr // 7) * BaseDKP
    # 醉虾
    defaultrw += num.zx * BaseDKP
    # 血战海河
    defaultrw += num.jh * BaseDKP
    # 帮派战场
    defaultrw += num.zc * BaseDKP
    # 掠夺
    defaultrw += num.ld * BaseDKP
    # 争锋
    defaultrw += num.zf * BaseDKP * 2
    return defaultrw


def rw(dkp):
    if dkp == 0:
        return 0
    elif dkp >= 8 * BaseDKP:
        return 8
    else:
        return dkp//BaseDKP


class ItemRecord:
    def __init__(self):
        self.id = ''  # ID
        self.ga = ''  # 帮派
        self.wr = 0  # 委任
        self.zx = 0  # 醉虾
        self.jh = 0  # 血战海河
        self.zc = 0  # 帮派战场
        self.ld = 0  # 掠夺
        self.zf = 0  # 争锋


UnionNameList = []
with open("LianMeng_DKP.txt", 'r', encoding='utf-8') as LMD:
    for l in LMD.readlines():
        if "本周" in l or "PVE" in l or "PVP" in l:
            pass
        elif "消耗" in l:
            pass
        else:
            UnionNameList.append(cvl(l).split('\t'))

# 格式 ID 帮派
UnionNameDict = {UnionNameList[i][0]: UnionNameList[i][1] for i in range(len(UnionNameList))}
print(UnionNameDict)
Temp = [[] for x in range(600)]
with open("LianMeng_DKPModifyRecord.txt", 'r', encoding='utf-8') as DKPRecord:
    cot = 0
    for l in DKPRecord.readlines():
        if not l == '\n':
            Temp[cot].append(l)
        else:
            cot = cot + 1
    print("联盟总人数：", cot)
# print(Temp[cot-1]) 最后一人
ItemList = Temp[:cot - 1]

# 联盟DKP记录单周简化版详单写入
with open("SimDetails.txt", 'w', encoding='utf-8') as RecordSimple:
    for preid in ItemList:
        RecordSimple.write(preid[0])
        for x in preid[1:]:
            for d in weekdays:
                if d in x:
                    RecordSimple.write(str(x))

ItemEasy = []
for preid in ItemList:
    newItemRecord = ItemRecord()
    newRecord = ''
    newItemRecord.id = preid[0].split()[0]
    try:
        newItemRecord.ga = UnionNameDict[newItemRecord.id]
    except KeyError:
        print("KeyError: Can't find the key item:" + newItemRecord.id)
        time.sleep(5)
    else:
        pass
    # print(newItemRecord.ga)
    for x in preid[1:]:
        for d in weekdays:
            if d in x:
                newRecord += str(x.split())
                # print(newRecord)
                newItemRecord.wr = newRecord.count('帮派委任')
                newItemRecord.zx = newRecord.count('帮派醉侠')
                newItemRecord.jh = newRecord.count('血战海河')
                newItemRecord.zc = newRecord.count('帮派跨服战场')
                newItemRecord.ld = newRecord.count('掠夺战')
                newItemRecord.zf = newRecord.count('争锋战')
    ItemEasy.append(newItemRecord)

with open("ExcelData.txt", 'w', encoding='utf-8') as Simp:
    Simp.write("ID\t帮派\t委任\t醉侠\t血战\t战场\t掠夺\t争锋\n\tDKP\n\t箱子\n")
    for ind in ItemEasy:
        Simp.write(str(ind.id) + '\t' + str(ind.ga) + '\t' + str(ind.wr) + '\t' + str(ind.zx) + '\t' + str(
            ind.jh) + '\t' + str(ind.zc) + '\t' + str(ind.ld) + '\t' + str(ind.zf) + '\t' + str(event2dkp(ind)) + '\n')


