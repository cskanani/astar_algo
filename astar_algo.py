import queue,random
ol = queue.PriorityQueue() #openlist implimented with PriorityQueue to store non-visited nodes based on f value
cl = [] #closed list to store visited nodes
mvs = [] #list to store moves from root to goal
nexp = 0 #number of nodes explored
nvis = 0 #number of nodes visited
htyp = '' #hueristics type m = Manhatan, d = Displaced tiles, o = Over-estimated, any other for Zero hueristics
goal = [1,2,3,4,5,6,7,8,0]

#function for moving tile
def mv_u(p):
    arr=p.arr.copy()
    zi = arr.index(0)
    if(zi in [0,1,2]):
        return None
    else:
        arr[zi],arr[zi-3] =  arr[zi-3],arr[zi]
        return Node(p,arr,'u')
        
def mv_d(p):
    arr=p.arr.copy()
    zi = arr.index(0)
    if(zi in [6,7,8]):
        return None
    else:
        arr[zi],arr[zi+3] =  arr[zi+3],arr[zi]
        return Node(p,arr,'d')
        
def mv_l(p):
    arr=p.arr.copy()
    zi = arr.index(0)
    if(zi in [0,3,6]):
        return None
    else:
        arr[zi],arr[zi-1] =  arr[zi-1],arr[zi]
        return Node(p,arr,'l')
        
def mv_r(p):
    arr=p.arr.copy()
    zi = arr.index(0)
    if(zi in [2,5,8]):
        return None
    else:
        arr[zi],arr[zi+1] =  arr[zi+1],arr[zi]
        return Node(p,arr,'r')

#function for generating child-nodes
def gen_c(parent):
    global nexp
    mu = mv_u(parent)
    md = mv_d(parent)
    ml = mv_l(parent)
    mr = mv_r(parent)
    if (mu != None): ol.put(mu);nexp+=1
    if (md != None): ol.put(md);nexp+=1
    if (ml != None): ol.put(ml);nexp+=1
    if (mr != None): ol.put(mr);nexp+=1
    
#function for calculating different type of hueristics
def find_h(arr):
    h = 0
    if(htyp == 'm'):
        for i in range(1,9):
            pos = arr.index(i)
            x = pos//3
            y = pos%3
            posg = goal.index(i)
            xg = posg//3
            yg = posg%3
            h += abs(xg-x) + abs(yg-y)
    elif(htyp == 'd'):
        for i in range(1,9):
            if(arr[i-1] != i): 
                h += 1
    elif(htyp == 'o'):
        return random.randint(1000,2000)
    else:
        return 0
    return h

#class for creating node objects
class Node:
    def __init__(self,parent,arr,mv):
        self.parent = parent
        self.mv = mv
        self.g = parent.g+1 if (parent != None) else 0
        self.h = find_h(arr)
        self.f = self.g+self.h
        self.arr = arr
        
    def __lt__(self, other):
        return self.f < other.f
     
#taking initial state from user
sarr = [int(x) for x in input('arr : ').split(' ')]

#function to run a_star algo
def run_as(m):
    global htyp, nmvs, nvis
    nexp = 0
    htyp = m
    mvs[:] = []
    cl[:] = []
    ol.queue.clear()
    
    s = Node(None,sarr,'')
    ol.put(s)

    while(not ol.empty()):
        nvis += 1
        p = ol.get()
        if(p.arr == goal):
            while(p.parent != None):
                mvs.insert(0,p.mv)
                p = p.parent
            break
        if p in cl:
            continue
        gen_c(p)
        cl.append(p.arr)

#funvtion for printing results data
def p_data(m):
    print('\n')
    if(htyp == 'm'):
        print('Data with Manhatan hueristics : ')
    elif(htyp == 'd'):
        print('Data with displaced tiles hueristics : ')
    elif(htyp == 'o'):
        print('Data with over-estimated hueristics : ')
    else:
        print('Data with zero hueristics : ')
    print('Number of nodes explored :',nexp)
    print('Number of nodes visited :',nvis)
    print('Length of path :',len(mvs))
    print('Path to goal :',mvs)

run_as('m');p_data('m')
run_as('d');p_data('d')
run_as('z');p_data('z')
run_as('o');p_data('o')
