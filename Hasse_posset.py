import random


def BFS(A, jobs, s):
    n = len(jobs)
    Q = [s]
    F = []
    while Q:
        v = Q[0]
        for w in range(n):
            if (v, w) in A and w not in F and w not in Q:
                Q.append(w)
        Q.remove(v)
        F.append(v)
    return F


def checkTransitivity(arc, arcList, jobs):
    A = arcList.copy()
    A.remove(arc)
    i = arc[0]
    j = arc[1]
    B = BFS(A, jobs, i)
    if j in B:
        return True
    else:
        return False


def addTransitiveArcs(arcs):
    flag = False
    n = len(arcs)
    for i in range(n):
        for j in range(i + 1, n):
            a = arcs[i][0]
            b = arcs[i][1]
            c = arcs[j][0]
            d = arcs[j][1]
            if b == c and (a, d) not in arcs:
                arcs.append((a, d))
                flag = True
    arcs.sort()
    if flag:
        arcs = addTransitiveArcs(arcs)
    return arcs


J = range(7)
jobs = [j for j in J]
n = len(jobs)
allArcs = []

# select 5 random prec which are not tranitive
# Parameterized Precedent constarint

n_prec = 5
ro = [j for j in J]
random.shuffle(ro)

posCons = []
for i in J:
    for j in range(i + 1, n):
        posCons.append((ro[i], ro[j]))
prec = random.sample(posCons, n_prec)
prec.sort()

for arc in prec:
    if checkTransitivity(arc, prec, jobs):
        prec.remove(arc)

while len(prec) < n_prec:
    newArc = random.choice(posCons)
    if newArc not in prec:
        prec.append(newArc)
        prec.sort()
        for arc in prec:
            if checkTransitivity(arc, prec, jobs):
                prec.remove(arc)

# transitive prec arcs
precTrans = prec.copy()
precTrans = addTransitiveArcs(precTrans)
trans = precTrans.copy()
for i in precTrans:
    if i in prec:
        trans.remove(i)

# incomparable pairs
incomp = []
for i in posCons:
    if i not in precTrans:
        incomp.append(i)

# output prec
cons = ""
for (i, j) in prec:
    cons += "{} \prec {}, ".format(i + 1, j + 1)
cons = cons[:-2]

# output transitive arcs
transArcs = "{"
for (i, j) in trans:
    transArcs += "({},{}), ".format(i + 1, j + 1)

if not trans:  # in case there is no transitive arc return {}
    transArcs = transArcs + "}"
else:
    transArcs = transArcs[:-2] + "}"

# output incomparable pairs
incomp.sort()
incoPairs = "{"
for (i, j) in incomp:
    incoPairs += "({},{}), ".format(i + 1, j + 1)
if not incomp:
    incoPairs = incoPairs + "}"
else:
    incoPairs = incoPairs[:-2] + "}"

########### Chain and AntiChain ############

# Chain code and function
prec_inc = []

for (i, j) in prec:
    prec_inc.append((i + 1, j + 1))

prec_chain = {}
for elements in prec_inc:
    if elements[0] in prec_chain:
        prec_chain[elements[0]].append(elements[1])
    else:
        prec_chain[elements[0]] = [elements[1]]

G_chain = prec_chain


def DFS(G, v, seen=None, path=None):
    if seen is None: seen = []
    if path is None: path = [v]

    seen.append(v)

    paths = []
    if v in G.keys():
        for t in G[v]:
            if t not in seen:
                t_path = path + [t]
                paths.append(tuple(t_path))
                paths.extend(DFS(G, t, seen[:], t_path))
                # print(paths)

    return paths


chain_all = []
for i in range(1, 8):
    chain_all.append(DFS(G_chain, i))

length_chain = []
for i in chain_all:
    for j in i:
        length_chain.append(len(j))

l_chain = random.randint(max(length_chain) - 1, max(length_chain))
chain = []

for elements in chain_all:
    for element in elements:
        if len(element) == l_chain:
            chain.append(element)

### Formating Chain ###
Chain = "{"
for j in chain:
    Chain += str(j)
    Chain += str(",")

if not chain:
    Chain = Chain + "}"
else:
    Chain = Chain[:-1] + "}"

#### Code and Function for AntiChain ####
prec_inc = []
prec_inc_rev = []

for (i, j) in prec:
    prec_inc.append((i + 1, j + 1))
    prec_inc_rev.append((j + 1, i + 1))

prec_anti = {}
for elements in prec_inc:
    if elements[0] in prec_anti:
        prec_anti[elements[0]].append(elements[1])
    else:
        prec_anti[elements[0]] = [elements[1]]

prec_anti_rev = {}
for elements in prec_inc_rev:
    if elements[0] in prec_anti_rev:
        prec_anti_rev[elements[0]].append(elements[1])
    else:
        prec_anti_rev[elements[0]] = [elements[1]]

G_in = prec_anti
G_out = prec_anti_rev
Jobs_anti = [i for i in range(1, 8)]
jobs_anti = [] + Jobs_anti


def Anti_Chain(G_in, G_out, jobs_anti, v, seen=None, non_comp=None, path=None, comp=None):
    if v is None: v = 1
    if seen is None: seen = []
    if comp is None: comp = []
    if non_comp is None: non_comp = []
    if path is None: path = [v]

    seen.append(v)
    paths = []

    if v in G_in.keys():
        for i in G_in[v]:
            if i not in non_comp:
                non_comp.append(i)

    if v in G_out.keys():
        for i in G_out[v]:
            if i not in non_comp:
                non_comp.append(i)

    for j in jobs_anti:
        if j not in seen and j not in non_comp and j not in comp and j > max(seen):
            comp.append(j)

    for u in comp:
        t_path = path + [u]
        paths.append(tuple(t_path))
        paths.extend(Anti_Chain(G_in, G_out, jobs_anti, u, seen[:], non_comp[:], t_path, comp=None))

    return paths


antichain_all = []
for i in range(1, 8):
    antichain_all.append(Anti_Chain(G_in, G_out, jobs_anti, i))

length_anti = []
for i in antichain_all:
    for j in i:
        length_anti.append(len(j))

l_anti = random.randint(max(length_anti) - 1, max(length_anti))
antichain = []

for elements in antichain_all:
    for element in elements:
        if len(element) == l_anti:
            antichain.append(element)

### Formating Chain ###
Antichain = "{"
for j in antichain:
    Antichain += str(j)
    Antichain += str(",")

if not antichain:
    Antichain = Antichain + "}"
else:
    Antichain = Antichain[:-1] + "}"

##### Checking Intree and Outtree #####

# check intree
intree = True
for i in prec_anti.keys():
    if len(prec_anti[i]) > 1:
        intree = False
intree = str(intree)

# Check Outtree
outtree = True
for i in prec_anti_rev.keys():
    if len(prec_anti_rev[i]) > 1:
        outtree = False
outtree = str(outtree)

##### Additional Questions #####
# a) Number of Transitive arcs

number_of_trans = len(trans)

# b) Is (a,b,c) is Chain or AntiChain ?

l_a = 3
anti_l = []
for elements in antichain_all:
    for element in elements:
        if len(element) >= l_a:
            anti_l.append(element)

l_c = 2

chain_l = []
for elements in chain_all:
    for element in elements:
        if len(element) >= l_c:
            chain_l.append(element)

chain_antichain = anti_l + chain_l
value = random.sample(chain_antichain, 1)

result = []
if value[0] in anti_l:
    result.append('antichain')

else:
    result.append('chain')

