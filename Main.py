import FileIO

data = FileIO.RecordData()


def readCommand():
    cmd = list(input().split())
    if cmd[0] == 'exit':
        exit()
    elif cmd[0] == 'reset':
        data.reset()
    elif cmd[0] == 'query':
        data.queryTime()
    elif cmd[0] == 'going':
        data.printGoingList()
    elif cmd[0] == 'leave':
        data.printLeaveList()
    else:
        if not (cmd[0] in data.headList):
            print('Invalid Header')
            print()
            return
        hour = int(cmd[1]) // 100
        minu = int(cmd[1]) % 100
        if hour < 0 or hour > 23 or minu < 0 or minu > 59:
            print('Invalid Time')
            print()
            return
        data.saveCommand(cmd)


if __name__ == '__main__':
    while True:
        if readCommand():
            break
