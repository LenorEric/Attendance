import StringList
import os
import datetime
import time
import NameList
import xlwt


def returnName(data):
    return data[0]


def minusTime(timeMus):
    hour0 = int(timeMus[0]) // 100
    minu0 = int(timeMus[0]) % 100
    hour1 = int(timeMus[1]) // 100
    minu1 = int(timeMus[1]) % 100
    return hour1 * 60 + minu1 - minu0 - hour0 * 60


class RecordData:
    headList = ['卢婧', '钱浩文', '马驰原', '张沈浩']
    head = {headList[0]: 0, headList[1]: 1, headList[2]: 2, headList[3]: 3}
    revHead = {0: headList[0], 1: headList[1], 2: headList[2], 3: headList[3]}
    onGoingList = []  # 存组号
    dataList = []
    week = ''
    TOTAL = 720

    def __init__(self):
        self.onGoingList = []
        self.dataList = []
        self.week = ''
        cfg = open('config.ini', 'r')
        self.week = cfg.readline()
        if self.week != str(datetime.datetime.now().year) + str(time.strftime("%W")) + '.dat':
            print("It's a new week, maybe you want to reset?")
        if not (os.path.exists(os.path.join('data', self.week))):
            open(os.path.join('data', self.week), 'w')
            return
        data = open(os.path.join('data', self.week), 'r')
        while True:
            datum = data.readline()
            if datum:
                self.dataList.append(StringList.String2List(datum))
            else:
                break
        self.getOnGoingList()

    def readData(self):
        if not (os.path.exists(os.path.join('data', self.week))):
            open(os.path.join('data', self.week), 'w')
            return
        data = open(os.path.join('data', self.week), 'r')
        while True:
            datum = data.readline()
            if datum:
                self.dataList.append(StringList.String2List(datum))
            else:
                break

    def getOnGoingList(self):
        count = [0] * 4
        self.onGoingList = []
        for i in range(len(self.dataList)):
            count[self.head[self.dataList[i][0]]] = 1 - count[self.head[self.dataList[i][0]]]
        for i in range(4):
            if count[i] == 1:
                self.onGoingList.append(i)

    def calcTime(self, headName):
        time1 = [0, 0]
        switch = 0
        count = 0
        for i in range(len(self.dataList)):
            if self.dataList[i][0] == headName:
                time1[switch] = self.dataList[i][1]
                switch = 1 - switch
                if switch == 0:
                    count += minusTime(time1)
        return count

    def printGoingList(self):
        self.getOnGoingList()
        if not (len(self.onGoingList)):
            print("No group ongoing")
            print()
        for i in range(len(self.onGoingList)):
            for j in range(len(self.dataList)):
                if self.dataList[-1 - j][0] == self.revHead[self.onGoingList[i]]:
                    print(self.dataList[-1 - j])
                    break
        print()

    def printLeaveList(self):
        upon = [0] * 4
        leaveList = []
        for i in range(len(self.dataList)):
            upon[self.head[self.dataList[i][0]]] = 1 - upon[self.head[self.dataList[i][0]]]
            if upon[self.head[self.dataList[i][0]]]:
                if len(self.dataList[i]) > 3:
                    timeMus = [self.dataList[i][1], 0]
                    for t in range(i + 1, len(self.dataList)):
                        if self.dataList[t][0] == self.dataList[i][0]:
                            timeMus[1] = self.dataList[t][1]
                            break
                    timeLeave = minusTime(timeMus)
                    for j in range(3, len(self.dataList[i]), 2):
                        # print(data[i], ' 请假了，理由是： ', data[i + 1])
                        for name in NameList.nameSplit(self.dataList[i][j]):
                            if timeLeave > 0:
                                leaveList.append([name, self.dataList[i][j + 1], timeLeave])
        leaveList.sort(key=returnName)
        if len(leaveList) == 0:
            print("No leave")
            print()
            return
        presentName = leaveList[0][0]
        altogetherLeave = 0
        leaverous = []
        for leave in leaveList:
            if leave[0] == presentName:
                altogetherLeave += leave[2]
                leaverous.append([leave[1], leave[2]])
            else:
                print()
                print(presentName, "请假了共计", altogetherLeave // 60, "小时", altogetherLeave % 60, "分钟:")
                for lvs in leaverous:
                    print("    因 ", lvs[0], "请假了", lvs[1] // 60, "小时", lvs[1] % 60, "分钟")
                presentName = leave[0]
                altogetherLeave = leave[2]
                leaverous = [leave[1:3]]
        print()
        print(presentName, "请假了共计", altogetherLeave // 60, "小时", altogetherLeave % 60, "分钟:")
        for lvs in leaverous:
            print("    因 ", lvs[0], "请假了", lvs[1] // 60, "小时", lvs[1] % 60, "分钟")
        print()

    def queryTime(self):
        for i in range(4):
            remainderTime = self.calcTime(self.revHead[i])
            print(self.revHead[i], ' 小组已经学习了 ', remainderTime // 60, ' 小时， ', remainderTime % 60, ' 分钟。')
            remainderTime = self.TOTAL - remainderTime
            if remainderTime > 0:
                print('本周还需自习至少 ', remainderTime // 60, ' 小时， ', remainderTime % 60, ' 分钟。')
            else:
                print('本周学习任务已经完成')
            print()

    def calcPresentTime(self, name):
        remainder = [0, 0]
        for i in range(len(self.dataList)):
            if self.dataList[i][0] == name:
                remainder[0] = remainder[1]
                remainder[1] = self.dataList[i][1]
        return minusTime(remainder)

    def saveCommand(self, cmd):
        data = open(os.path.join('data', self.week), 'a')
        data.write(str(cmd))
        data.write('\n')
        self.dataList.append(cmd)
        if self.head[cmd[0]] in self.onGoingList:
            print()
            self.onGoingList.remove(self.head[cmd[0]])
            time1 = self.calcTime(cmd[0])
            time2 = self.calcPresentTime(cmd[0])
            print(cmd[0], ' 小组本次已经学习了 ', time2 // 60, ' 小时， ', time2 % 60, ' 分钟。')
            time1 = self.TOTAL - time1
            if time1 > 0:
                print('本周还需自习至少 ', time1 // 60, ' 小时， ', time1 % 60, ' 分钟。')
            else:
                print('本周学习任务已经完成')
            print()
        else:
            print()
        self.getOnGoingList()

    def reset(self):
        week = str(datetime.datetime.now().year) + str(time.strftime("%W")) + '.dat'
        cfg = open('config.ini', 'w')
        cfg.write(week)
        cfg.close()
        self.onGoingList = []
        self.getOnGoingList()
        self.dataList = []
        self.readData()
        self.week = week
        if not (os.path.exists(os.path.join('data', self.week))):
            data = open(os.path.join('data', self.week), 'w')
            data.close()
        print('Reset')
        print()

    def export(self):
        def saveSheet(*args):
            column = 0
            nonlocal row
            for item in args:
                sheet.write(row, column, str(item), style)
                column += 1
            row += 1

        def saveSheet2(*args):
            column = 6
            nonlocal row
            for item in args:
                sheet.write(row, column, str(item), style)
                column += 1
            row += 1

        row = 0
        exp = xlwt.Workbook(encoding='utf-8')
        sheet = exp.add_sheet('本周自习情况')
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = '等线'
        style.font = font
        sheet.col(0).width = 6000
        sheet.col(7).width = 5000
        for i in range(4):
            remainderTime = self.calcTime(self.revHead[i])
            saveSheet(self.revHead[i] + ' 小组已经学习了 ', remainderTime // 60, ' 小时， ', remainderTime % 60, ' 分钟。')
            remainderTime = self.TOTAL - remainderTime
            if remainderTime > 0:
                saveSheet('本周还需自习至少 ', remainderTime // 60, ' 小时， ', remainderTime % 60, ' 分钟。')
            else:
                saveSheet('本周学习任务已经完成')
            saveSheet()
        row = 0
        upon = [0] * 4
        leaveList = []
        for i in range(len(self.dataList)):
            upon[self.head[self.dataList[i][0]]] = 1 - upon[self.head[self.dataList[i][0]]]
            if upon[self.head[self.dataList[i][0]]]:
                if len(self.dataList[i]) > 3:
                    timeMus = [self.dataList[i][1], 0]
                    for t in range(i + 1, len(self.dataList)):
                        if self.dataList[t][0] == self.dataList[i][0]:
                            timeMus[1] = self.dataList[t][1]
                            break
                    timeLeave = minusTime(timeMus)
                    for j in range(3, len(self.dataList[i]), 2):
                        # print(data[i], ' 请假了，理由是： ', data[i + 1])
                        for name in NameList.nameSplit(self.dataList[i][j]):
                            if timeLeave > 0:
                                leaveList.append([name, self.dataList[i][j + 1], timeLeave])
        leaveList.sort(key=returnName)
        if len(leaveList) == 0:
            saveSheet2("No leave")
            saveSheet2()
            week = str(datetime.datetime.now().year) + str(time.strftime("%W")) + '.xls'
            exp.save(os.path.join('C:\\Users\\EC\\Desktop', week))
            return
        presentName = leaveList[0][0]
        altogetherLeave = 0
        leaverous = []
        for leave in leaveList:
            if leave[0] == presentName:
                altogetherLeave += leave[2]
                leaverous.append([leave[1], leave[2]])
            else:
                saveSheet2()
                saveSheet2(presentName, "请假了共计", altogetherLeave // 60, "小时", altogetherLeave % 60, "分钟:")
                for lvs in leaverous:
                    saveSheet2("    因 ",str(lvs[0]) + '  请假了', lvs[1] // 60, "小时", lvs[1] % 60, "分钟")
                presentName = leave[0]
                altogetherLeave = leave[2]
                leaverous = [leave[1:3]]
        saveSheet2()
        saveSheet2(presentName, "请假了共计", altogetherLeave // 60, "小时", altogetherLeave % 60, "分钟:")
        for lvs in leaverous:
            saveSheet2("    因 ", str(lvs[0]) + '  请假了', lvs[1] // 60, "小时", lvs[1] % 60, "分钟")
        saveSheet2()
        week = str(datetime.datetime.now().year) + str(time.strftime("%W")) + '.xls'
        exp.save(os.path.join('C:\\Users\\EC\\Desktop', week))
