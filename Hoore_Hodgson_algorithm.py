import random

jobs = range(5)

processing_time = [4, 4, 4, 4, 7]
due_date = [11, 12, 17, 11, 20]

# for i in jobs:
#       processing_time.append(random.randint(3,7))
#       due_date.append(random.randint(9,20))

# Sort the jobs in non-decreasing order of Due_Dates
jobs_sorted_due_date = [j for _, j in sorted(zip(due_date, jobs))]


# Function return job with maximum processing time
def find_max_pro_job(avail_job):
    temp = []
    for i in avail_job:
        temp.append([processing_time[i], i])

    return sorted(temp)[-1][1]


early_jobs = []
late_jobs = []
temp = {}
t = 0

# Calculation of U_j and getting the schedule
## In case of tie of new job and early job, new job would be schedule last and early jobs would be remained unchanged
for j in jobs_sorted_due_date:

    if (t + processing_time[j] <= due_date[j]):
        early_jobs.append(j)
        t = t + processing_time[j]
    else:
        remove_job = find_max_pro_job(early_jobs)
        if (processing_time[j] >= processing_time[remove_job]):
            late_jobs.append(j)
        else:
            early_jobs.append(j)
            t = t + processing_time[j] - processing_time[remove_job]
            late_jobs.append(remove_job)
            early_jobs.remove(remove_job)
    print(early_jobs, late_jobs)

S = early_jobs + sorted(late_jobs)

# output schedule
schedule = "("
for i in S:
    schedule += "{},".format(i + 1)
schedule = schedule[:-2] + ")"

# Objective value of U_j
objective_value = len(late_jobs)