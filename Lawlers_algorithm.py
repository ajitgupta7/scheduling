import random

# Initialization of jobs, processing times and due_dates
Jobs = [j for j in range(6)]
p = []
d = []

for i in Jobs:
    p.append(random.randint(1, 5))
    d.append(random.randint(1, 15))


# functions for adding transitive arcs
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


# define multiple functions to select from
# we can keep adding new functions here
def f1(x, t):
    return (1 if t > d[x] else 0)


def f2(x, t):
    return (t)


def f3(x, t):
    return (t - d[x])


def f4(x, t):
    return ((max(0, t - d[x])) ^ 2 + 1)


def f5(x, t):
    return (t - 1)


# selecting 4 functions at random from the list of functions
functions = [
    [f1, '\ f_j(C_j)  = U_j = \\left\{ \\begin{array}{rcl} 0 &  C_j \leq d_j, \\ 1 & C_j > d_j \end{array}\\right.'],
    [f2, '\ f_j(C_j) = C_j'],
    [f3, '\ f_j(C_j) = L_j  = C_j-d_j'],
    [f4, '\ f_j(C_j) = T^2_j + 1 = (max\{0,C_j-d_j\})^2 +1'],
    [f5, '\ f_j(C_j) = C_j - 1']]

func = random.sample(functions, 4)

# fmax calculation function
seq = [s for s in range(6)]
random.shuffle(seq)


def fmax_cal(x, t):
    if x == seq[0]:
        return (func[0][0](x, t))
    if x == seq[1] or x == seq[2]:
        return (func[1][0](x, t))
    if x == seq[3] or x == seq[4]:
        return (func[2][0](x, t))
    if x == seq[5]:
        return (func[3][0](x, t))


# Parameterized Precedent constarint
ro = [j for j in range(6)]
random.shuffle(ro)

posCons = []
for i in range(6):
    for j in range(i + 1, len(ro)):
        posCons.append((ro[i], ro[j]))
prec = random.sample(posCons, 4)
prec.sort()

# values which are not in precedent constraints
jobs_in_prec = [j for s in prec for j in s]
x = list(set(Jobs) - set(jobs_in_prec))

# converting precedents to dictnary
prec_con = {}
for elements in prec:
    if elements[0] in prec_con:
        prec_con[elements[0]].append(elements[1])
    else:
        prec_con[elements[0]] = [elements[1]]

# getting the starting elements for algoritham
# having no successor
c1 = [j for j in prec_con.keys()]
c2 = [j for j in prec_con.values()]
start = list(set(c1) - set(set([j for elements in c2 for j in elements])))

if len(x) > 0:
    for i in x:
        start.append(i)

# Calculation of schedules
S = []
J1 = [] + start
T = sum(p)
Temp = []
L = []

while len(S) < 6:
    for j in J1:
        Temp.append(fmax_cal(j, T))
    new_job = [job for _, job in sorted(zip(Temp, J1))][0]
    L.append([job for job, _ in sorted(zip(Temp, J1))][0])
    Temp.clear()
    S.append(new_job)
    J1.remove(new_job)
    T = T - p[new_job]
    for x in S:
        if x in prec_con.keys():
            for k in prec_con[x]:
                if k not in S:
                    J1.append(k)

    J1 = [j for j in set(J1)]

# additing transitive arcs
precTrans = prec.copy()
precTrans = addTransitiveArcs(precTrans)

precedents = ""
for (i, j) in precTrans:
    precedents += "{} \prec {}, ".format(i + 1, j + 1)
precedents = precedents[:-2]

# formating for questions and presentation
seq = [j + 1 for j in seq]
S = S[::-1]
S = [j + 1 for j in S]
schedule = "(" + ",".join(map(str, tuple(S))) + ")"
f_max = max(L)