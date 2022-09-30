import copy
import numpy as np

#visited is a set(), graph is a dictionary {:[]}, node is a node name. 
#this will work to see what nodes can be reached
def dfs(visited, graph, node):  
    if node not in visited:
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)
    return visited

#root is a node, graph is a dict, nodes is a list of nodes
#This will be used to see what nodes can reach the root
#It can test all other nodes in the graph or just the indicated nodes.
def rch(root, graph, nodes=None):
    reach = set()
    if nodes==None:
        for node in graph.keys():
            visited = set()
            x = dfs(visited, graph, node)
            if root in x: 
                reach.add(node)
    else:
        for node in nodes:
            visited = set()
            x = dfs(visited, graph, node)
            if root in x: 
                reach.add(node)
    return reach

#undir is the undirected graph, partg is the current instance of the digraph,
#i is the current node to add
#This takes one undirected edges of i and adds a valid direction, then goes to
#the next and adds a valid direction, etc; returns list of graphs
def orientations(undir, partg, i):
    #edges to be added
    ug = undir[i]
    #only adds edges to lesser nodes
    for k in ug:
        if k>i:
            ug.remove(k)
    #list of graphs
    ans = []
    ######
    #ug is edges to be added, t is current graph, i1 is node to be added, j is
    #stepper variable to know when is done
    def generate(ug, t, i1, j):
        #copies needed for recursion
        tg=copy.deepcopy(t)
        tg1=copy.deepcopy(t)
        #set of reachable nodes form i1
        R = dfs(set(), t, i1)
        #nodes less than i1 that reach i1
        nn = list(range(1, i1, 1))
        B = rch(i1, t, nn)
        #recursion base case: it added all edges and has a valid graph
        if j==len(ug):
            new = copy.deepcopy(t)
            ans.append(new)
            return
        #in case an edge is not to be added yet
        #might be useless thanks to line 55
        if ug[j]>i:
            generate(ug,t, i1,j+1)
        #in case the edge cannot be added
        #i thing this never happens (i kinda proofed it)
        if (ug[j] in R) and (ug[j] in B): 
            return
        #first recursion: the node doesnt reach i1, we add (i1,j) and rec.
        if ug[j] not in B: 
            tg1[i1].append(ug[j])
            generate(ug, tg1, i1, j+1)
        #second recursion: the node isnt reachable by i1, we add (j,i1) and rec.
        if ug[j] not in R: 
            tg[ug[j]].append(i1)
            generate(ug, tg, i1, j+1)
    ######
    #start the recursion with suitable variables and current graph. 
    ptg = copy.deepcopy(partg)
    generate(ug, ptg, i, 0)
    return ans

#undir is the undirected graph, direct is the base directed graph, 
#partg is the current directed graph, i is the current node to be added, n is
#number of nodes, total is the counter
def acyclic(undir, direct, partg, i, nodes, total):
    #rec base case: it added all and is an acyclic orientation
    if i>nodes:
        total.append(copy.deepcopy(partg))
        return
    #add to partg the directed edges of i
    partg[i]=copy.deepcopy(direct[i])
    #get all possible orientations of edges from i in partg
    possible = copy.deepcopy(orientations(undir, partg, i))
    #if none is found (I think this doesnt happen), stop recursion
    if len(possible)==0: return
    #if some are found, for each we continue the acyclic completition
    for orpart in possible:
        new = copy.deepcopy(orpart)
        acyclic(undir, direct, new, i+1, nodes, total)
    return

##########################################
#Climb 
#Returns climb of a monomial
#a is a list (represents a monomial)
def climb(a):
    b1 = 0
    s = 0
    for b2 in a:
        if b2>b1:
            s+=b2-b1
        b1=b2
    return s

#Empty support
#Returns the monomials a,b,c st. u=a+c, v=b+c and a,b have empty support intersection. 
#Returns a list with the monomials.
#u, v lists (monomials) with the same length 
def supp(u, v):
    if len(u)==len(v):
        a = [0]*len(u)
        b = [0]*len(u)
        c = [0]*len(u)
        i = 0
        while i<len(u):
            #The same amount on both, they become 0
            if u[i]==v[i]:
                a[i] = 0
                b[i] = 0
                c[i] = u[i]
            #u bigger, v becomes zero
            elif u[i] > v[i]:
                a[i] = u[i]-v[i]
                b[i] = 0
                c[i] = v[i]
            #v bigger, u becomes zero
            elif v[i] > u[i]:
                a[i] = 0
                b[i] = v[i]-u[i]
                c[i] = u[i]
            i+=1
    diff = [a,b,c]
    return(diff)

#Generate all monomials in m variables with climb less than or equal to h
#Returns dictionary of monomials, ans, with keys numbers
#a is a monomial used in the recursion, m number of variables >0, h max climb >0
def mon(ans, a, h, m, j):
    if j==m-1:
        i=0
        while i<=h:
            a[j]=i
            if climb(a)<=h:
                k = len(ans)
                ans[k+1]=copy.deepcopy(a)
            i+=1
    else:
        i=0
        while i<=h:
            a[j]=i
            mon(ans,a,h,m,j+1)
            i+=1
    return(ans)

#Get all edges in the graph, differentiating directed, undirected
#Returns: dictionary, dg, with directed edges (only principal)
#ug, with undirected edges
#gg, empty graph with the appropiate keys. 
#principal, list of principal undirected edges
#relations, dictionary with the related edges
def edges(vert, h):
    #Directed
    dg = {}
    #Undirected
    ug = {}
    #Empty
    gg = {}
    #List of principal edges
    principal = []
    #Related edges
    relation = {}
    for x in vert.keys():
        #Directed edges
        dg[x] = []
        #Undirected edges 
        ug[x] = []
        #Empty graph
        gg[x] = []
    for x in vert.keys():
        for y in vert.keys():
            if x<y:
                n = supp(vert[x], vert[y])
                #Only add those with climb lesst than h in separation
                if climb(n[0]) + climb(n[1]) <= h:
                    #First is contained in second
                    if n[0] == [0]*len(n[0]):
                        dg[x].append(y)
                    #Second is contained in first
                    elif n[1] == [0]*len(n[1]):
                        dg[y].append(x)
                    #Nothing is between them, a pcpal edge
                    elif n[2] == [0]*len(n[2]):
                        ug[y].append(x)
                        principal.append((x,y))
                        relation[(x,y)]=[]
                    #None of the ones before, but still an edge in the graph
                    else:
                        a = [ky for ky,val in vert.items() if val == n[0]][0]
                        b = [ky for ky,val in vert.items() if val == n[1]][0]
                        try:
                            aa = relation[(a,b)]
                        except:
                            aa = []
                            relation[(a,b)] = aa
                        aa.append((x,y))
                        # ug[y].append(x)
    return([dg,ug,gg, principal, relation])
##########################################

#List of vertices with the monomials they represent
test1 =  mon({},[0]*5,2,5,0)
#List of graphs needed and list of principal edges and related edges
test = edges(test1,2)

# #Testing of the graph
# print(test1)
# print("------------------------------------------------")
# for k,v in test[0].items(): print(k,v)
# print()
# for k,v in test[1].items(): print(k,v)
# print()
# for k,v in test[2].items(): print(k,v)
# print()
# print(test[3])
# print()
# for k,v in test[4].items(): print(k,v)
# print()

# print('------------------------------------------------')


##########################################################

#Checks if a cycle starting in start exists
#Returns True if no cycle exists, False if it exists
#start is starting node
#node is current node, graph is the graph, visited is list of reached nodes
def rec(start, node, graph, visited):
    response = True
    for i in graph[node]:
        #Checks if it went back to the start node
        if i == start:
            return False
        #Avoids checking nodes twice
        if i not in visited:
            #List the next node as visited
            visited.append(i)
            #Recursion
            response = rec(start, i, graph, visited)
    #Returns variable with response
    return response

#####################################
#List to store acyclic orientations
answer = []
#Gets all acyclic orientations with the principal edges
acyclic(test[1], test[0], test[2], 1, len(test[1]), answer)

print('Orientations only with principal edges:',len(answer))
print('------------------------------------------------')
#List of acyclic orientations with all the edges
final = []
#Testing of the initial acyclic orientations
final2 = []
#Checks each acyclic orientation
for gg in answer:
    g=copy.deepcopy(gg)
    #Assumes first it is acyclic
    acy = True
    #Testing that the initial directed graph is acyclic
    # for k in g.keys():
    #     if acy: acy = rec(k,k,g,[k])
    # if acy: final2.append(g)
    
    #Get a pcpal edge
    for ed in test[3]:
        #if it goes from 0 to 1
        if ed[1] in g[ed[0]]:
            #add the related edges with correct orientation
            for es in test[4][ed]:
                g[es[0]].append(es[1])
        #if it goes from 1 to 0
        elif ed[0] in g[ed[1]]:
           #add the related edges with correct orientation
           for es in test[4][ed]:
               g[es[1]].append(es[0])
        #if this happens it is wrong!!
        else:
            print('error')
    #Check if acyclic with all the edges of the graph
    acy = True
    for k in g.keys():
        if acy: acy = rec(k,k,g,[k])
    #Add the full directed graph if it is acyclic
    if acy: final.append(g)

# print('Acyclic orientations with only principal edges:', len(final2))
# print('----------------------')
print('Acyclic orientations with all edges:',len(final))
print('------------------------------------------------')
# A in farkas lemma variant

#Difference of two monomials. Used for the matrix of the principal edges. 
def difMon(init, fi):
    inM = test1[init]
    fiM = test1[fi]
    out = [0]*len(inM)
    for i in range(len(inM)):
        out[i] = inM[i]-fiM[i]
    return out

# matrices = []

# for curr in final:
#     A = np.zeros((len(test[3])+len(test1[1]),len(test1[1])))
#     i=0
#     while i < len(test1[1]):
#         A[i][i] = 1
#         i+=1
#     for ed in test[3]:
#         if ed[0] in curr[ed[1]]:
#             A[i]=difMon(ed[0], ed[1])
#         else:
#             A[i]=difMon(ed[1], ed[0])
#         i+=1
#     matrices.append(A)
#     print('-----------------')
#     print(np.transpose(A))
#     B = np.zeros(len(A))
#     for i in range(len(A)):
#         B[i] = np.sum(A[i])
#     print('1+2+3:', B)
#     B = np.zeros(len(A))
#     for i in range(len(A)):
#         B[i] = A[i][0]+A[i][1]
#     print('1+2:', B)
#     B = np.zeros(len(A))
#     for i in range(len(A)):
#         B[i] = A[i][0]+A[i][2]
#     print('1+3:', B)
#     B = np.zeros(len(A))
#     for i in range(len(A)):
#         B[i] = A[i][1]+A[i][2]
#     print('2+3:', B)














