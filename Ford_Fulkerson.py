# importing libraries
import random
import math

''' Functions'''


def createIntervals(p_j, r_j, r_n1):
    r = r_j.copy()
    r.append(r_n1)
    Intervals = []
    for i in range(len(r) - 1):
        interval = [r[i], r[i + 1]]
        Intervals.append(interval)
    return Intervals


def createFlowNetwork(jobs, p_j, r_j, Intervals):
    n = 2 + len(jobs) + len(Intervals)
    Interval_cap_m = [I[1] - I[0] for I in Intervals]
    Interval_cap_all = [m * Interval_cap_m[i] for i in range(len(Interval_cap_m))]
    graphCap = [[0 for i in range(n)] for j in range(n)]
    for i in range(len(jobs)):
        graphCap[0][i + 1] = p_j[i]
        for j in range(i, len(Intervals)):
            graphCap[i + 1][len(jobs) + j + 1] = Interval_cap_m[j]
    for j in range(len(Intervals)):
        graphCap[len(jobs) + j + 1][n - 1] = Interval_cap_all[j]
    return graphCap


def listNodes(jobs, Intervals):
    nodes = ["s"]
    for i in range(len(jobs)):
        nodes.append("j_" + str(i + 1))
    for i in range(len(Intervals)):
        nodes.append("I_" + str(i + 1))
    nodes.append("t")
    return nodes


def listEdges(nodes, flowNetwork):
    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if flowNetwork[i][j]:
                edges.append((nodes[i], nodes[j]))
    return edges


def BFS(graph, s, t, parent):
    # Return True if there is node that has not iterated.
    visited = [False] * len(graph)
    queue = []
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.pop(0)
        for ind in range(len(graph[u])):
            if visited[ind] is False and graph[u][ind] > 0:
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u
    return True if visited[t] else False


def FordFulkerson(graph, source, sink):
    # This array is filled by BFS and to store path
    parent = [-1] * (len(graph))
    max_flow = 0
    while BFS(graph, source, sink, parent):
        path_flow = float("Inf")
        s = sink
        while s != source:
            # Find the minimum value in select path
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
        parent = [-1] * (len(graph))
    return (max_flow, graph)


def checkFeasibility(nodes, flowNetwork):
    necFlow = 0
    for i in range(len(nodes)):
        necFlow += flowNetwork[0][i]
    FF = FordFulkerson(flowNetwork, 0, len(flowNetwork) - 1)
    maxFlow = FF[0]
    if maxFlow == necFlow:
        feasible = True
    else:
        feasible = False
    return feasible


def computeFlow(G, remainingCap):
    flow = []
    for i in range(len(G)):
        flow.append([])
        for j in range(len(G[i])):
            if G[i][j]:
                temp = G[i][j] - remainingCap[i][j]
                flow[i].append(temp)
            else:
                flow[i].append(0)
    return flow


'''PART 1'''

# assiging the jobs, processing time and release time
jobs = [j for j in range(1, 6)]
p_j = []
r_j = []

for i in range(len(jobs)):
    p_j.append(random.randint(2, 7))
r_j.append(0)
for i in range(len(jobs) - 1):
    r_j.append(random.randint(0, 5))
r_j.sort()

# randomly decising number of machines
m = random.randint(2, 3)

# choose lambda
p_r_j = [p_j[j] + r_j[j] for j in range(len(jobs))]
lam = max(p_r_j) + 1

# Intervals
Intervals = createIntervals(p_j, r_j, lam)
intervals = "{"
for i in Intervals:
    intervals += str(i) + ", "
intervals = intervals[:-2] + "}"

# Flow Network
flowNetwork = createFlowNetwork(jobs, p_j, r_j, Intervals)
nodes = listNodes(jobs, Intervals)
edges = listEdges(nodes, flowNetwork)

# Questions about edge cost
selEdges = random.sample(edges, 2)
e1 = selEdges[0]
e2 = selEdges[1]
index_1_0 = nodes.index(e1[0])
index_1_1 = nodes.index(e1[1])
index_2_0 = nodes.index(e2[0])
index_2_1 = nodes.index(e2[1])
c_1 = flowNetwork[index_1_0][index_1_1]
c_2 = flowNetwork[index_2_0][index_2_1]

# Output edges
e_1 = "(" + str(e1[0]) + "," + str(e1[1]) + ")"
e_2 = "(" + str(e2[0]) + "," + str(e2[1]) + ")"

# Check feasibility
feasible = checkFeasibility(nodes, flowNetwork)
if feasible:
    feasible_true = "YES"
    feasible_false = "NO"
else:
    feasible_true = "NO"
    feasible_false = "YES"

''' PART 2 '''

# assiging the jobs, processing time and release time
p_j_new = []
r_j_new = []

for i in range(len(jobs)):
    p_j_new.append(random.randint(2, 7))
r_j_new.append(0)
for i in range(len(jobs) - 1):
    r_j_new.append(random.randint(0, 5))
r_j_new.sort()

# choose lambda
p_r_j_new = [p_j_new[j] + r_j_new[j] for j in range(len(jobs))]
lam_new = max(p_r_j_new)
feasible_new = False

while not feasible_new:
    Intervals_new = createIntervals(p_j_new, r_j_new, lam_new)
    flowNetwork_new = createFlowNetwork(jobs, p_j_new, r_j_new, Intervals_new)
    # maintain original flow network as G
    G = []
    for i in range(len(flowNetwork_new)):
        G.append([])
        for j in range(len(flowNetwork_new[i])):
            G[i].append(flowNetwork_new[i][j])
    nodes_new = listNodes(jobs, Intervals_new)
    feasible_new = checkFeasibility(nodes_new, flowNetwork_new)
    if not feasible_new:
        lam_new += 1
# copy list G
H = []
for i in range(len(G)):
    H.append([])
    for j in range(len(G[i])):
        H[i].append(G[i][j])
FF = FordFulkerson(H, 0, len(H) - 1)
maxFlow_new = FF[0]
remainingCap = FF[1]
flow = computeFlow(G, remainingCap)

# output new intervals
intervals_new = "\{"
for i in Intervals_new:
    intervals_new += str(i) + ", "
intervals_new = intervals_new[:-2] + "\}"

# preliminary work for schedule creation
MV = [[] for i in range(len(Intervals_new))]
IntLoad = [[0 for i in range(len(jobs))] for j in range(len(Intervals_new))]
for j in range(len(Intervals_new)):
    for i in range(len(jobs)):
        load = flow[i + 1][len(jobs) + j + 1]
        IntLoad[j][i] = load
        for l in range(load):
            MV[j].append(i + 1)
# wrap values (Interval name and its wrap values)
q = []
for i in range(len(Intervals_new)):
    q.append(Intervals_new[i][1] - Intervals_new[i][0])

# create schedule
schedule = [[] for i in range(m)]
for i in range(len(Intervals_new)):
    T = 0
    for j in range(m):
        for k in range(q[i]):
            if T < len(MV[i]):
                schedule[j].append(MV[i][T])
            else:
                schedule[j].append(0)
            T += 1

# formating schedule
M1 = schedule[0]
M2 = schedule[1]
if m >= 3:
    M3 = schedule[2]
else:
    M3 = []

sol_m1 = "("
for i in M1:
    sol_m1 += str(i) + ", "
sol_m1 = sol_m1[:-2] + ")"

sol_m2 = "("
for i in M2:
    sol_m2 += str(i) + ", "
sol_m2 = sol_m2[:-2] + ")"

sol_m3 = "("
for i in M3:
    sol_m3 += str(i) + ", "
if M3:
    sol_m3 = sol_m3[:-2]
sol_m3 += ")"

# calculate c_max
c_max = 0
for i in range(len(M1)):
    if M1[i] > 0:
        if i >= c_max:
            c_max = i + 1