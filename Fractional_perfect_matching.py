# importing libraries
import random
import math

# assiging the jobs, processing time and release time
jobs = [j for j in range(1, 6)]
p_j = []
r_j = []

for i in range(len(jobs)):
    p_j.append(random.randint(2, 7))
    r_j.append(random.randint(0, 5))

r_j.sort()

# r_n1 = 15

# randomly decising number of machines
m = random.randint(2, 3)

# getting the C_max value
p_r_j = [p_j[j] + r_j[j] for j in range(len(jobs))]

r_n1 = random.randint(max(p_r_j), max(p_r_j) + 1)

# Creating the intervals
r_j.append(r_n1)
Intervals = []
for i in range(len(r_j) - 1):
    interval = [i + 1, r_j[i], r_j[i + 1]]
    if r_j[i + 1] > r_j[i]:
        Intervals.append(interval)

Interval_cost = [I[2] - I[1] for I in Intervals]

# Matrix will contain jobs order, there flow to Intervals
matrix = [[]]
matrix = [[0 for i in range(len(jobs))] for j in range(len(Intervals))]

## Greedly calculating the flow in the auxilary network
for j in jobs:
    flow = p_j[j - 1]
    temp = []

    for i in range(len(Intervals)):
        if flow > 0 and Intervals[i][0] >= j:
            if flow > Interval_cost[i]:
                matrix[i][j - 1] = Interval_cost[i]
                flow = flow - Interval_cost[i]
            else:
                matrix[i][j - 1] = flow
                flow = flow - Interval_cost[i]

# wrap values (Interval name and its wrap values)
q = []
for i in range(len(Intervals)):
    q.append([Intervals[i][0], max(matrix[i])])

# Creating MV which will contain all jobs name as they
# are assigned to the particular intervals

MV = []
T = 0

for i in range(len(Intervals)):

    T += q[i][1] * m

    for j in range(len(jobs)):
        temp = matrix[i][j]
        while temp:
            MV.append(j)
            temp = temp - 1
    while len(MV) < T:
        MV.append(-1)

MV = [j + 1 for j in MV]

## Assigning the jobs to machines (depending upon 2 or 3 machines)
if m == 2:
    M1 = []
    M2 = []
if m == 3:
    M1 = []
    M2 = []
    M3 = []

T = 0

for i in range(len(Intervals)):
    qi = q[i][1]
    for t in range(qi):
        if m == 2:
            M1.append(MV[T + t])
            M2.append(MV[qi + T + t])
        if m == 3:
            M1.append(MV[T + t])
            M2.append(MV[qi + T + t])
            M3.append(MV[2 * qi + T + t])

    T = T + qi * m

while len(M1) < r_n1:
    if m == 2:
        M1.append(0)
        M2.append(0)
    if m == 3:
        M1.append(0)
        M2.append(0)
        M3.append(0)

M = []

if m == 2:
    M.append(M1)
    M.append(M2)

if m == 3:
    M.append(M1)
    M.append(M2)
    M.append(M3)

n_sol = ""
for i in range(m):
    n_sol += "("
    for t in range(r_n1):
        n_sol += "{}".format(M[i][t])
        n_sol += ","
    n_sol = n_sol[:-1]
    n_sol += "),"
n_sol = n_sol[:-1]

# 2) interval wrap values
q_wrap = random.sample(q, 2)
q_wrap.sort()
q_wrap_val = (q_wrap[0][1], q_wrap[1][1])
q_wrap