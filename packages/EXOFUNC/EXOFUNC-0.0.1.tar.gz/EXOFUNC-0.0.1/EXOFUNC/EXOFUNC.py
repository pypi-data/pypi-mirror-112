def SUM(list):
    list.append(0)
    print("SUM = ", sum(list))

def AVG(list, noi):
    list.append(0)
    print("AVG = ", (sum(list)/noi))

def COUNT(list):
    print("COUNT = ", len(list))

def MAX(list):
    list.sort()
    print("MAX = ", list[-1])

def MIN(list):
    list.sort()
    print("MIN = ", list[1])