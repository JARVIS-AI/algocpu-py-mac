"""
CPU Scheduling Algorithms in Python
Author: Amir Mohammad Safari
Repository: https://github.com/JARVIS-AI/algocpu-py-mac
Description: This program implements FCFS, SJF, Round Robin, and MLFQ scheduling algorithms.
             Users can enter process details and choose a scheduling algorithm to run.

License: MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
"""

import hashlib

# Original author name and content hash for verification
AUTHOR_NAME = "Amir Mohammad Safari"
ORIGINAL_HASH = "d41d8cd98f00b204e9800998ecf8427e"  # Replace with actual hash of the file content

def verify_integrity():
    with open(__file__, 'rb') as f:
        file_content = f.read()
    current_hash = hashlib.md5(file_content).hexdigest()
    
    if current_hash != ORIGINAL_HASH or AUTHOR_NAME != "Amir Mohammad Safari":
        raise ValueError("File integrity compromised or author name altered.")

# Call the integrity check function at the beginning
verify_integrity()


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
    for process in processes:
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


def get_process_input():
    num_processes = int(input("Enter number of processes: "))
    processes = []
    for i in range(num_processes):
        print(f"\nProcess {i + 1}:")
        burst_time = int(input("Enter burst time: "))
        arrival_time = int(input("Enter arrival time: "))
        processes.append(Process(pid=i + 1, burst_time=burst_time, arrival_time=arrival_time))
    return processes


def main():
    print("Choose a scheduling algorithm:")
    print("1. FCFS (First-Come, First-Served)")
    print("2. SJF (Shortest Job First)")
    print("3. Round Robin")
    print("4. MLFQ (Multi-Level Feedback Queue)")
    choice = int(input("Enter your choice (1-4): "))

    processes = get_process_input()

    if choice == 1:
        print("\nFCFS Scheduling")
        fcfs(processes)
    elif choice == 2:
        print("\nSJF Scheduling")
        sjf(processes)
    elif choice == 3:
        quantum = int(input("Enter time quantum for Round Robin: "))
        print("\nRound Robin Scheduling")
        round_robin(processes, quantum)
    elif choice == 4:
        num_queues = int(input("Enter number of queues for MLFQ: "))
        queues = [[] for _ in range(num_queues)]
        time_quantum = []
        for i in range(num_queues):
            tq = int(input(f"Enter time quantum for queue {i + 1}: "))
            time_quantum.append(tq)
            num_in_queue = int(input(f"Enter number of processes in queue {i + 1}: "))
            for j in range(num_in_queue):
                queues[i].append(processes[j])
        print("\nMLFQ Scheduling")
        mlfq(processes, queues, time_quantum)
    else:
        print("Invalid choice!")
        return

    # Display results
    print("\nProcess\tBurst Time\tArrival Time\tWaiting Time\tTurnaround Time")
    for p in processes:
        print(f"{p.pid}\t{p.burst_time}\t\t{p.arrival_time}\t\t{p.waiting_time}\t\t{p.turnaround_time}")


if __name__ == "__main__":
    main()
