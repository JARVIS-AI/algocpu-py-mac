class Process:
    def __init__(self, pid, burst_time, arrival_time=0, priority=0):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.priority = priority


def fcfs(processes):
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    for process in processes:
        if time < process.arrival_time:
            time = process.arrival_time
        time += process.burst_time
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    return processes


def sjf(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    time = 0
    for process in sorted(processes, key=lambda x: (x.arrival_time, x.burst_time)):
        if time < process.arrival_time:
            time = process.arrival_time
        time += process.burst_time
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    return processes


def round_robin(processes, quantum):
    time = 0
    queue = processes[:]
    while queue:
        process = queue.pop(0)
        if process.arrival_time <= time:
            if process.remaining_time > quantum:
                time += quantum
                process.remaining_time -= quantum
                queue.append(process)
            else:
                time += process.remaining_time
                process.remaining_time = 0
                process.completion_time = time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
        else:
            queue.append(process)
            time += 1
    return processes


def mlfq(processes, queues, time_quantum):
    time = 0
    for queue_level in range(len(queues)):
        queue = queues[queue_level]
        for process in queue:
            if process.arrival_time <= time:
                if process.remaining_time > time_quantum[queue_level]:
                    time += time_quantum[queue_level]
                    process.remaining_time -= time_quantum[queue_level]
                    if queue_level < len(queues) - 1:
                        queues[queue_level + 1].append(process)
                else:
                    time += process.remaining_time
                    process.remaining_time = 0
                    process.completion_time = time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
    return processes


# Example usage:
process_list = [
    Process(pid=1, burst_time=5, arrival_time=0),
    Process(pid=2, burst_time=3, arrival_time=1),
    Process(pid=3, burst_time=8, arrival_time=2),
    Process(pid=4, burst_time=6, arrival_time=3)
]

print("FCFS:")
for p in fcfs(process_list):
    print(f"Process {p.pid}: Waiting Time = {p.waiting_time}, Turnaround Time = {p.turnaround_time}")

print("\nSJF:")
for p in sjf(process_list):
    print(f"Process {p.pid}: Waiting Time = {p.waiting_time}, Turnaround Time = {p.turnaround_time}")

print("\nRound Robin:")
for p in round_robin(process_list, quantum=2):
    print(f"Process {p.pid}: Waiting Time = {p.waiting_time}, Turnaround Time = {p.turnaround_time}")

print("\nMLFQ:")
queues = [[process_list[0], process_list[1]], [process_list[2], process_list[3]]]
time_quantum = [2, 4]
for p in mlfq(process_list, queues, time_quantum):
    print(f"Process {p.pid}: Waiting Time = {p.waiting_time}, Turnaround Time = {p.turnaround_time}")
