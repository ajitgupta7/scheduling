# importing libraries
import random
import math

# assiging the jobs, processing time and release time
jobs = [j for j in range(1, 6)]
# p_j = [2,7,2,3,2]
# r_j = [0,0,2,3,5]

for i in range(len(jobs)):
    p_j.append(random.randint(2, 6))

r_j = []

for i in range(len(jobs) - 1):
    r_j.append(random.randint(1, 5))
print(r_j)

while len(set(r_j)) < 3:
    r_j.clear()
    for i in range(len(jobs) - 1):
        r_j.append(random.randint(1, 5))

r_j.append(0)

r_j.sort()

# r_n1 = 15

# randomly decising number of machines
# m = random.randint(2,3)
m = 3

# getting the C_max value
p_r_j = [p_j[j] + r_j[j] for j in range(len(jobs))]

lb = max(r_j) + max(p_j)
ub = max(r_j) + sum(p_j)

# r_n1 = int((lb+ub)/2)
lam = max(p_r_j) + 1


def AuxiliaryMaxFlow(p_j, r_j, r_n1):
    # Creating the intervals
    r = r_j.copy()
    r.append(r_n1)
    Intervals = []
    for i in range(len(r) - 1):
        interval = [i + 1, r[i], r[i + 1]]
        Intervals.append(interval)

    Interval_cap_m = [I[2] - I[1] for I in Intervals]
    Interval_cap_all = [m * Interval_cap_m[i] for i in range(len(Interval_cap_m))]

    # Matrix will contain jobs order, there flow to Intervals
    matrix = [[]]
    matrix = [[0 for i in range(len(jobs))] for j in range(len(Intervals))]

    print(Interval_cap_all, Interval_cap_m)

    # Greedly calculating the flow in the auxilary network
    for j in jobs:
        flow = p_j[j - 1]
        for i in range(len(Intervals)):
            if flow > 0 and Intervals[i][0] >= j:
                if flow > Interval_cap_all[i]:
                    push = min(Interval_cap_all[i], Interval_cap_m[i])
                else:
                    push = min(flow, Interval_cap_m[i])
                matrix[i][j - 1] = push
                flow -= push
                Interval_cap_all[i] -= push

    # wrap values (Interval name and its wrap values)
    q = []
    for i in range(len(Intervals)):
        q.append([Intervals[i][0], max(math.ceil(sum(matrix[i]) / m), max(matrix[i]))])
    # Creating MV which will contain all jobs name as they
    # are assigned to the particular intervals
    print(matrix)

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
    print(MV)

    ## Assigning the jobs to machines (depending upon 2 or 3 machines)
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
        M1.append(0)
        M2.append(0)
        if M3:
            M3.append(0)

    if sum(x > 0 for x in M2) == 0:
        M2.clear()
    if M3:
        if sum(x > 0 for x in M3) == 0:
            M3.clear()

    # calculate c_max
    c_max = 0
    for i in range(len(M1)):
        if M1[i] > 0:
            if i > c_max:
                c_max = i
    c_max += 1
    return (M1, M2, M3, q, c_max)




