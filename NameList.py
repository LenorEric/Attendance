def nameToList():
    name = []
    read = input()
    while read != '#':
        name.append(read)
        read = input()
    name.sort()
    return name


nameList = ['丁嘉铭', '乐言', '余志沛', '余昊昱', '刘博原', '刘正阳', '刘育甫', '刘胜楠', '卢婧', '周磊', '唐昊旸', '唐梓睿', '张沈浩', '张逸飞', '朱泽佳', '李新宇',
            '李行展', '杨文博', '毛妍', '游静溦', '漆育均', '潘泓任', '王子涵', '王珂', '程阳', '蒋超杰', '郭浩哲', '钱浩文', '陈子锐', '马宇轩', '马驰原', '高毅凡']


def nameSplit(names):
    nameSplited = []
    for name in nameList:
        if name in names:
            nameSplited.append(name)
    return nameSplited


if __name__ == '__main__':
    nameSplit('我喜欢你呀')
