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
    else:
        if not (cmd[0] in data.headList):
            print('Invalid Header')
            return
        hour = int(cmd[1]) // 100
        minu = int(cmd[1]) % 100
        if hour < 0 or hour > 23 or minu < 0 or minu > 59:
            print('Invalid Time')
            return
        data.saveCommand(cmd)


if __name__ == '__main__':
    while True:
        if readCommand():
            break
