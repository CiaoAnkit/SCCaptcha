import math
def test_dist(a,b,path):
    if a[0] is None or b[0] is None or a[1] is None or b[1] is None:
        print(path)   
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) #has a problem TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) #has a problem TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'


