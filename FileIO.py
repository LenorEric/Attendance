import StringList
import os
import datetime


def minusTime(time):
    hour0 = int(time[0]) // 100
    minu0 = int(time[0]) % 100
    hour1 = int(time[1]) // 100
    minu1 = int(time[1]) % 100
    return hour1 * 60 + minu1 - minu0 - hour0 * 60


class RecordData:
    headList = ['卢婧', '周磊', '李麻子', '张三']
    head = {headList[0]: 0, headList[1]: 1, headList[2]: 2, headList[3]: 3}
    revHead = {0: headList[0], 1: headList[1], 2: headList[2], 3: headList[3]}
    onGoingList = []  # 存组号
    dataList = []
    week = ''
    TOTAL = 960

    def __init__(self):
        self.onGoingList = []
        self.dataList = []
        self.week = ''
        cfg = open('config.ini', 'r')
        self.week = cfg.readline()
        if self.week != str(datetime.datetime.now().year) + str(
                datetime.datetime.strptime('20190825', '%Y%m%d').strftime('%W')) + '.dat':
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

    def getOnGoingList(self):
        count = [0 for i in range(4)]
        for i in range(len(self.dataList)):
            count[self.head[self.dataList[i][0]]] = 1 - count[self.head[self.dataList[i][0]]]
        for i in range(4):
            if count[i] == 1:
                self.onGoingList.append(i)

    def calcTime(self, headName):
        time = [0, 0]
        switch = 0
        count = 0
        for i in range(len(self.dataList)):
            if self.dataList[i][0] == headName:
                time[switch] = self.dataList[i][1]
                switch = 1 - switch
                if switch == 0:
                    count += minusTime(time)
        return count

    def printGoingList(self):
        if not (len(self.onGoingList)):
            print("No group ongoing")
        for i in range(len(self.onGoingList)):
            for j in range(len(self.dataList)):
                if self.dataList[-1 - j][0] == self.revHead[self.onGoingList[i]]:
                    print(self.dataList[-1 - j])
                    break

    def queryTime(self):
        for i in range(4):
            time = self.calcTime(self.revHead[i])
            print(self.revHead[i], ' 小组已经学习了 ', time // 60, ' 小时， ', time % 60, ' 分钟。')
            time = self.TOTAL - time
            if time >= 0:
                print('本周还需自习至少 ', time // 60, ' 小时， ', time % 60, ' 分钟。')
            else:
                print('本周学习任务已经完成')
            print()

    def saveCommand(self, cmd):
        data = open(os.path.join('data', self.week), 'a')
        data.write(str(cmd))
        data.write('\n')
        self.dataList.append(cmd)
        if self.head[cmd[0]] in self.onGoingList:
            self.onGoingList.remove(self.head[cmd[0]])
            time = self.calcTime(cmd[0])
            print(cmd[0], ' 小组已经学习了 ', time // 60, ' 小时， ', time % 60, ' 分钟。')
            time = self.TOTAL - time
            if time >= 0:
                print('本周还需自习至少 ', time // 60, ' 小时， ', time % 60, ' 分钟。')
            else:
                print('本周学习任务已经完成')
            print()
        self.getOnGoingList()

    def reset(self):
        week = str(datetime.datetime.now().year) + str(
            datetime.datetime.strptime('20190825', '%Y%m%d').strftime('%W')) + '.dat'
        cfg = open('config.ini', 'w')
        cfg.write(week)
        cfg.close()
        self.onGoingList = []
        self.dataList = []
        data = open(os.path.join('data', self.week), 'w')
        data.close()
        print('Reset')
