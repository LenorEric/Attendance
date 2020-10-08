# Changing String with List
def String2List(c_str):
    c_str = c_str.replace('\n', '')
    c_str = c_str.replace(' ', '')
    c_str = c_str.replace("'", '')
    return String2ListIter(c_str)[0]


def isNotRev(ch):
    if ch == '[' or ch == ']' or ch == ',':
        return False
    else:
        return True


def String2ListIter(subLine):
    subTree = []
    if subLine == "":
        return subTree
    strT = ''
    i = 0
    while i < len(subLine):
        strT = ''
        if subLine[i] == '[':
            tx = 1
            for j in range(i + 1, len(subLine)):
                if subLine[j] == '[':
                    tx += 1
                elif subLine[j] == ']':
                    tx -= 1
                if not tx:
                    break
            subTree.append(String2ListIter(subLine[i + 1:j]))
            i = j
        elif isNotRev(subLine[i]):
            while i < len(subLine) and isNotRev(subLine[i]):
                strT = strT + subLine[i]
                i += 1
            subTree.append(strT)
        i += 1
    return subTree
