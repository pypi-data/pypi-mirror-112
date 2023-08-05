def pycellHelp():
    print("PYCELL FUNCTIONS:")
    print("sumList(list)")
    print("avgList(list, numberOfItems)")
    print("countList(list)")
    print("maxList(list)")
    print("minList(list)")
def sumList(list):
    list.append(0)
    print("SUM: ", sum(list))
def avgList(list, numberOfItems):
    list.append(0)
    print("AVG: ", (sum(list)/numberOfItems))
def countList(list):
    print("COUNT: ", len(list))
def maxList(list):
    list.sort()
    print("MAX: ", list[-1])
def minList(list):
    list.sort()
    print("MIN: ", list[1])