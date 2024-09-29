# Get number of jobs from the user
num_jobs = int(input("Enter number of jobs: "))

# Input job deadlines and execution times
jobs = []
for i in range(num_jobs):
    deadline = int(input(f"Enter deadline for job {i+1}: "))
    exec_time = int(input(f"Enter execution time for job {i+1}: "))
    jobs.append((deadline, exec_time, i+1))

# Sort jobs by deadline
jobs.sort(key=lambda x: x[0])

# Perform earliest deadline first (EDF) scheduling
time = 0
completed_jobs = []

for deadline, exec_time, job_id in jobs:
    if time + exec_time <= deadline:
        time += exec_time
        completed_jobs.append(job_id)

# Output the jobs that can be completed by their deadlines
print(f"\nJobs completed by their deadlines: {completed_jobs}")
