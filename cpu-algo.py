import tkinter as tk
from tkinter import messagebox

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 30
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#f7f1e2", relief="solid", borderwidth=1)
        label.grid()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = None




# FCFS Scheduling Function
def fcfs_scheduling(processes, arrival_times, burst_times):
    n = len(processes)
    waiting_times = [0] * n
    turnaround_times = [0] * n

    # Calculate Waiting Time
    for i in range(1, n):
        waiting_times[i] = burst_times[i - 1] + waiting_times[i - 1] - arrival_times[i] + arrival_times[i - 1]
        if waiting_times[i] < 0:
            waiting_times[i] = 0

    # Calculate Turnaround Time
    for i in range(n):
        turnaround_times[i] = burst_times[i] + waiting_times[i]

    # Calculate Average Waiting Time and Turnaround Time
    avg_waiting_time = sum(waiting_times) / n
    avg_turnaround_time = sum(turnaround_times) / n

    return waiting_times, turnaround_times, avg_waiting_time, avg_turnaround_time






# MLFQ Scheduling Function
def mlfq_scheduling(processes, arrival_times, burst_times, quantum_times):
    n = len(processes)
    max_queue_level = len(quantum_times)
    queues = [[] for _ in range(max_queue_level)]
    
    remaining_burst = burst_times[:]
    waiting_times = [0] * n
    turnaround_times = [0] * n
    time = 0
    completed = 0
    last_execution_time = [-1] * n
    
    current_process_idx = 0
    
    while completed < n:
        while current_process_idx < n and arrival_times[current_process_idx] <= time:
            queues[0].append(current_process_idx)
            current_process_idx += 1

        executed_process = False
        for q in range(max_queue_level):
            if queues[q]:
                process_id = queues[q].pop(0)
                quantum = quantum_times[q]
                
                if last_execution_time[process_id] != -1:
                    waiting_times[process_id] += time - last_execution_time[process_id]
                
                executed_process = True
                if remaining_burst[process_id] > quantum:
                    time += quantum
                    remaining_burst[process_id] -= quantum
                    last_execution_time[process_id] = time
                    
                    if q + 1 < max_queue_level:
                        queues[q + 1].append(process_id)
                    else:
                        queues[q].append(process_id)
                else:
                    time += remaining_burst[process_id]
                    turnaround_times[process_id] = time - arrival_times[process_id]
                    waiting_times[process_id] = turnaround_times[process_id] - burst_times[process_id]
                    remaining_burst[process_id] = 0
                    last_execution_time[process_id] = time
                    completed += 1
                
                break
        
        if not executed_process and current_process_idx < n:
            time = arrival_times[current_process_idx]

    avg_waiting_time = sum(waiting_times) / n
    avg_turnaround_time = sum(turnaround_times) / n
    
    return waiting_times, turnaround_times, avg_waiting_time, avg_turnaround_time






# Round Robin Scheduling Function
def round_robin_scheduling(processes, arrival_times, burst_times, quantum):
    n = len(processes)
    remaining_burst = burst_times[:]
    waiting_times = [0] * n
    turnaround_times = [0] * n
    time = 0
    completed = 0
    queue = []
    process_index = 0

    while completed < n:
        # Add processes to the queue as they arrive
        while process_index < n and arrival_times[process_index] <= time:
            queue.append(process_index)
            process_index += 1

        if queue:
            process_id = queue.pop(0)

            if remaining_burst[process_id] > quantum:
                time += quantum
                remaining_burst[process_id] -= quantum
            else:
                time += remaining_burst[process_id]
                remaining_burst[process_id] = 0
                completed += 1
                turnaround_times[process_id] = time - arrival_times[process_id]
                waiting_times[process_id] = turnaround_times[process_id] - burst_times[process_id]

            # Add the process back to the queue if it's not finished
            if remaining_burst[process_id] > 0:
                queue.append(process_id)
        else:
            time = arrival_times[process_index]

    avg_waiting_time = sum(waiting_times) / n
    avg_turnaround_time = sum(turnaround_times) / n
    
    return waiting_times, turnaround_times, avg_waiting_time, avg_turnaround_time






# SJF Scheduling Function (Non-Preemptive)
def sjf_scheduling(processes, arrival_times, burst_times):
    n = len(processes)
    waiting_times = [0] * n
    turnaround_times = [0] * n
    completed = [False] * n
    time = 0
    completed_processes = 0
    
    while completed_processes < n:
        # Find the process with the smallest burst time among the available ones
        idx = -1
        min_burst = float('inf')
        
        for i in range(n):
            if not completed[i] and arrival_times[i] <= time and burst_times[i] < min_burst:
                min_burst = burst_times[i]
                idx = i
        
        if idx == -1:  # No process is available, so move time forward
            time += 1
            continue
        
        # Process idx is selected, update the times
        time += burst_times[idx]
        turnaround_times[idx] = time - arrival_times[idx]
        waiting_times[idx] = turnaround_times[idx] - burst_times[idx]
        completed[idx] = True
        completed_processes += 1
    
    # Calculate average waiting and turnaround times
    avg_waiting_time = sum(waiting_times) / n
    avg_turnaround_time = sum(turnaround_times) / n
    
    return waiting_times, turnaround_times, avg_waiting_time, avg_turnaround_time






# Function to handle button click and run the chosen scheduling algorithm
def run_scheduling():
    try:
        processes = [f"P{i+1}" for i in range(int(entry_processes.get()))]
        arrival_times = list(map(int, entry_arrival_times.get().split()))
        burst_times = list(map(int, entry_burst_times.get().split()))
        
        if len(arrival_times) != len(processes) or len(burst_times) != len(processes):
            raise ValueError("Number of processes, arrival times, and burst times should match.")
        
        if algorithm_choice.get() == "FCFS":
            waiting_times, turnaround_times, avg_waiting, avg_turnaround = fcfs_scheduling(processes, arrival_times, burst_times)
        
        elif algorithm_choice.get() == "MLFQ":
            quantum_times = list(map(int, entry_quantum_times.get().split()))
            waiting_times, turnaround_times, avg_waiting, avg_turnaround = mlfq_scheduling(processes, arrival_times, burst_times, quantum_times)
        
        elif algorithm_choice.get() == "RR":
            quantum = int(entry_quantum_times.get())
            waiting_times, turnaround_times, avg_waiting, avg_turnaround = round_robin_scheduling(processes, arrival_times, burst_times, quantum)
        
        elif algorithm_choice.get() == "SJF":
            waiting_times, turnaround_times, avg_waiting, avg_turnaround = sjf_scheduling(processes, arrival_times, burst_times)
        
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "Process\tArrival\tBurst\tWaiting\tTurnaround\n")
        result_box.insert(tk.END, "-" * 50 + "\n")

        for i in range(len(processes)):
            result_box.insert(tk.END, f"{processes[i]:<8}{arrival_times[i]:<8}{burst_times[i]:<8}{waiting_times[i]:<8}{turnaround_times[i]:<8}\n")

        result_box.insert(tk.END, "-" * 50 + "\n")
        result_box.insert(tk.END, f"Average Waiting Time: {avg_waiting:.2f}\n")
        result_box.insert(tk.END, f"Average Turnaround Time: {avg_turnaround:.2f}\n")

    
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))

# Function to toggle quantum time entry for MLFQ and RR
def toggle_quantum_times():
    if algorithm_choice.get() == "MLFQ" or algorithm_choice.get() == "RR":
        label_quantum_times.grid(row=4, column=0, padx=10, pady=10)
        entry_quantum_times.grid(row=4, column=1, padx=10, pady=10)
    else:
        label_quantum_times.grid_forget()
        entry_quantum_times.grid_forget()

# Function to show "About" information
def show_about():
    messagebox.showinfo("About", "Scheduling Algorithms App\nVersion 1.3\nCreated by [JARVIS-AI]")

# Create the main window
root = tk.Tk()
root.title("Scheduling Algorithms by JARVIS-AI")

# Disable maximize button
root.resizable(False, False)

# Load and set the icon (use a PNG file for macOS)
icon_image = tk.PhotoImage(file="/Users/jarvis/Downloads/chip.png")  # Update this with your image path
root.iconphoto(False, icon_image)

# Create a Menu bar
menu_bar = tk.Menu(root)

# Create a "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label=":)", command=show_about)

# Add the "Help" menu to the menu bar
menu_bar.add_cascade(label="Help and About App", menu=help_menu)

# Configure the window to display the menu
root.config(menu=menu_bar)

# Algorithm Choice (FCFS, MLFQ, or Round Robin or SJF)
algorithm_choice = tk.StringVar(value="FCFS")
label_choice = tk.Label(root, text="Choose Algorithm:")
label_choice.grid(row=0, column=0, padx=10, pady=10)

radio_fcfs = tk.Radiobutton(root, text="FCFS", variable=algorithm_choice, value="FCFS", command=toggle_quantum_times)
radio_fcfs.grid(row=0, column=1, padx=10, pady=10)

radio_mlfq = tk.Radiobutton(root, text="MLFQ", variable=algorithm_choice, value="MLFQ", command=toggle_quantum_times)
radio_mlfq.grid(row=0, column=2, padx=10, pady=10)

radio_rr = tk.Radiobutton(root, text="Round Robin", variable=algorithm_choice, value="RR", command=toggle_quantum_times)
radio_rr.grid(row=0, column=3, padx=10, pady=10)

radio_sjf = tk.Radiobutton(root, text="SJF", variable=algorithm_choice, value="SJF", command=toggle_quantum_times)
radio_sjf.grid(row=0, column=4, padx=10, pady=10)

# Process Entry
label_processes = tk.Label(root, text="Number of Processes:")
label_processes.grid(row=1, column=0, padx=10, pady=10)
entry_processes = tk.Entry(root)
entry_processes.grid(row=1, column=1, padx=10, pady=10)

# Arrival Times Entry
label_arrival_times = tk.Label(root, text="Arrival Times (space-separated):")
label_arrival_times.grid(row=2, column=0, padx=10, pady=10)
entry_arrival_times = tk.Entry(root)
entry_arrival_times.grid(row=2, column=1, padx=10, pady=10)

label1 = tk.Label(root, text="Hover on these")
label1.grid(row=1, column=3, padx=10, pady=10)

# Label 1 with border
label2 = tk.Label(root, text="Turnaround Time", bd=0.5, relief="solid", padx=5, pady=5)
label2.grid(row=2, column=3, padx=10, pady=10)
ToolTip(label2, "Turnaround Time: (Completion Time - Arrival Time)")

# Label 2 with border
label3 = tk.Label(root, text="Waiting Time", bd=0.5, relief="solid", padx=5, pady=5)
label3.grid(row=3, column=3, padx=10, pady=10)
ToolTip(label3, "Waiting Time: (Turnaround Time - Burst Time)")

# Burst Times Entry
label_burst_times = tk.Label(root, text="Burst Times (space-separated):")
label_burst_times.grid(row=3, column=0, padx=10, pady=10)
entry_burst_times = tk.Entry(root)
entry_burst_times.grid(row=3, column=1, padx=10, pady=10)

# Quantum Times Entry (for MLFQ or RR)
label_quantum_times = tk.Label(root, text="Quantum Times (MLFQ) or Quantum (RR):")
entry_quantum_times = tk.Entry(root)

# Result Box
result_box = tk.Text(root, height=10, width=50)
result_box.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Run Button
button_run = tk.Button(root, text="Run", command=run_scheduling)
button_run.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

# Start the application
root.mainloop()
