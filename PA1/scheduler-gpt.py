class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = None
        self.remaining_time = burst_time

    def __str__(self):
        return (f"Process {self.name}: Arrival Time: {self.arrival_time}, "
                f"Burst Time: {self.burst_time}, Wait Time: {self.wait_time}, "
                f"Turnaround Time: {self.turnaround_time}, Response Time: {self.response_time}")
    

def fifo_scheduling(processes):
    # Sort processes by their arrival time
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time  # If the CPU is idle, move forward in time
        process.wait_time = current_time - process.arrival_time
        process.turnaround_time = process.wait_time + process.burst_time
        process.response_time = process.wait_time  # In FIFO, wait time is the same as response time
        current_time += process.burst_time  # Move current time forward by the burst time of the process

    return processes

# Example usage:
processes_list = [Process('A', 0, 5), Process('B', 1, 4), Process('C', 4, 2)]
scheduled_processes = fifo_scheduling(processes_list)
for process in scheduled_processes:
    print(process)
