# Amari Terry

import json
import os
import sys

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.finish_time = -1

def parse_file(file_name):
    data = {
        "processes": [],
        "algorithm": None,
        "quantum": None,
        "processcount": None,
        "runfor": None
    }

    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith('processcount'):
                data['processcount'] = int(line.split()[1])
            elif line.startswith('runfor'):
                data['runfor'] = int(line.split()[1])
            elif line.startswith('use'):
                data['algorithm'] = line.split()[1]
            elif line.startswith('quantum'):
                data['quantum'] = int(line.split()[1])
            elif line.startswith('process'):
                parts = line.split()
                process_data = {
                    "name": parts[2],
                    "arrival": int(parts[4]),
                    "burst": int(parts[6])
                }
                data['processes'].append(process_data)
    
    # Validate required parameters
    if data['processcount'] is None:
        raise ValueError("Error: Missing parameter processcount")
    if data['runfor'] is None:
        raise ValueError("Error: Missing parameter runfor")
    if data['algorithm'] is None:
        raise ValueError("Error: Missing parameter algorithm")
    if data['algorithm'] == 'rr' and data['quantum'] is None:
        raise ValueError("Error: Missing quantum parameter when use is 'rr'")

    return data


def fifo_scheduler(num_processes, process_names, total_cpu_time, arrival_time, burst_time):
    process_queue = []
    start_time = [0] * num_processes
    finish_time = [0] * num_processes
    wait_time = [0] * num_processes
    turnaround_time = [0] * num_processes
    response_time = [0] * num_processes
    idle_times = []

    current_time = 0
    notRunning = True
    current_process = 0

    # All html was edited ChatGPT code 
    html_file = open("output.html","w")
    html_file.write("<html><body>")

    with open("output.txt", "w") as output_file:
     
        # Manually created
        output_file.write(str(num_processes).rjust(3)+" processes\n")
        output_file.write("Using First-Come First-Served\n")

        html_file.write("<p><font color= 'magenta'>"+str(num_processes).rjust(3)+" processes"+"</font></p>")
        html_file.write("<p><font color= 'teal'>"+"Using First-Come First-Served"+"</font></p>")

        # ChatGPT created but manually reformatted and rearranged
        while current_time < total_cpu_time:
            for i in range(num_processes):
                if arrival_time[i] == current_time:
                    output_file.write("Time "+str(current_time).rjust(3)+" : "+str(process_names[i]).rjust(2)+" arrived\n")
                    html_file.write("<p><font color= 'blue'>"+"Time "+str(current_time).rjust(3)+" : "+str(process_names[i]).rjust(2)+" arrived"+"</font></p>")
                    process_queue.append(i)

            # Manually created
            if notRunning == False:
                if finish_time[current_process] == current_time:
                    output_file.write("Time "+str(finish_time[current_process]).rjust(3)+" : "+str(process_names[current_process]).rjust(2)+" finished\n")
                    html_file.write("<p><font color= 'maroon'>"+"Time "+str(finish_time[current_process]).rjust(3)+" : "+str(process_names[current_process]).rjust(2)+" finished"+"</font></p>")
                    notRunning = True

            # ChatGPT created but manually reformatted and rearranged
            if len(process_queue) > 0:
                if  notRunning == True: 
                    current_process = process_queue.pop(0)
                    start_time[current_process] = current_time
                    output_file.write("Time "+str(start_time[current_process]).rjust(3)+" : "+str(process_names[current_process]).rjust(2)+" selected (burst "+str(burst_time[current_process]).rjust(3)+")\n")
                    html_file.write("<p><font color= 'green'>"+"Time "+str(start_time[current_process]).rjust(3)+" : "+str(process_names[current_process]).rjust(2)+" selected (burst "+str(burst_time[current_process]).rjust(3)+")"+"</font></p>")
                    finish_time[current_process] = start_time[current_process] + burst_time[current_process]

                    wait_time[current_process], turnaround_time[current_process], response_time[current_process] = metrics(arrival_time[current_process], start_time[current_process], finish_time[current_process])
                    notRunning = False

            # ChatGPT created but manually reformatted and rearranged with a little editing
            if len(process_queue)==0:
                if  notRunning == True:
                    output_file.write("Time "+str(current_time).rjust(3)+" : Idle\n")
                    html_file.write("<p><font color= 'navy'>"+"Time "+str(current_time).rjust(3)+" : Idle"+"</font></p>")

            

            current_time += 1

              
        output_file.write(f"Finished at time  {total_cpu_time}\n\n") 
        html_file.write("<p><font color= 'orangered'>"+"Finished at time  "+str(total_cpu_time)+"<br><br>"+"</font></p>")
           
       

        # ChatGPT created but manually reformatted
        for i in range(num_processes):
            if finish_time[i] != 0 and finish_time[i] < total_cpu_time:
                output_file.write(str(process_names[i]).rjust(2)+" wait "+str(wait_time[i]).rjust(3)+" turnaround "+str(turnaround_time[i]).rjust(3)+" response "+str(response_time[i]).rjust(3)+"\n")
                html_file.write("<p><font color= 'deeppink'>"+str(process_names[i]).rjust(2)+" wait "+str(wait_time[i]).rjust(3)+" turnaround "+str(turnaround_time[i]).rjust(3)+" response "+str(response_time[i]).rjust(3)+"</font></p>")

            
        # Manually created
        for i in range(num_processes):
            if finish_time[i] == 0 or finish_time[i] >= total_cpu_time:
                output_file.write(f"{process_names[i]} did not finish\n")  
                html_file.write("<p><font color= 'crimson'>"+process_names[i]+" did not finish"+"</font></p>")

        html_file.write("</body></html>")
        html_file.close()

# ChatGPT created with a little editing
def metrics(arrival_time, start_time, finish_time):
    wait_time = start_time - arrival_time
    turnaround_time = finish_time - arrival_time
    response_time = start_time - arrival_time
    return wait_time, turnaround_time, response_time
    

def preemptive_sjf(process_count, run_for, scheduling_algorithm, processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))

    current_time = 0
    completion_time = [0] * process_count
    turnaround_time = [0] * process_count
    waiting_time = [0] * process_count
    response_time = [0] * process_count

    print(f"{process_count} processes")
    print(f"Using preemptive {scheduling_algorithm}")

    timeline = set()
    selected_processes = set()

    while current_time < run_for or any(p.remaining_time > 0 for p in processes):
        ready_processes = [p for p in processes if p.remaining_time > 0 and p.arrival_time <= current_time]

        if not ready_processes:
            timeline.add((current_time, None, 'idle'))
            current_time += 1
            continue

        if scheduling_algorithm == "sjf":
            ready_processes.sort(key=lambda x: x.remaining_time)
        elif scheduling_algorithm == "fcfs":
            ready_processes.sort(key=lambda x: x.arrival_time)
        elif scheduling_algorithm == "rr":
            ready_processes.sort(key=lambda x: x.arrival_time)
        else:
            print("Invalid scheduling algorithm.")
            return

        selected_process = ready_processes[0]

        if selected_process.start_time == -1:
            selected_process.start_time = current_time
            response_time[int(selected_process.process_id[1:]) - 1] = current_time - selected_process.arrival_time

        selected_process.remaining_time -= 1
        current_time += 1

        if selected_process.remaining_time == 0 and selected_process not in selected_processes:
            selected_process.finish_time = current_time
            completion_time[int(selected_process.process_id[1:]) - 1] = current_time
            turnaround_time[int(selected_process.process_id[1:]) - 1] = selected_process.finish_time - selected_process.arrival_time
            waiting_time[int(selected_process.process_id[1:]) - 1] = turnaround_time[int(selected_process.process_id[1:]) - 1] - selected_process.burst_time

            timeline.add((current_time, selected_process, 'finished'))
            selected_processes.add(selected_process)
        elif selected_process not in selected_processes:
            timeline.add((current_time, selected_process, 'selected'))

    for process in processes:
        if process.arrival_time == process.start_time:
            timeline.add((process.arrival_time, process, 'arrived'))

    # Print timeline with chronological order and unique events
    current_event = None

    print("\nTimeline:")
    for time, event, event_type in sorted(timeline, key=lambda x: (x[0], x[2])):
        if event_type == 'arrived':
            print(f"Time  {event.arrival_time} : {event.process_id} arrived")
        elif event_type == 'selected':
            if event != current_event:
                print(f"Time  {time} : {event.process_id} selected (burst {event.burst_time})")
                current_event = event
        elif event_type == 'finished':
            print(f"Time  {time} : {event.process_id} finished")
        elif event_type == 'idle':
            print(f"Time  {time} : Idle")

    # Calculate and print statistics
    # print("\nStatistics:")
    for i in range(process_count):
        print(f"{processes[i].process_id} wait   {waiting_time[i]} turnaround   {turnaround_time[i]} response   {response_time[i]}")

    print(f"\nFinished at time  {current_time}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python scheduler-gpt.py <inputfile.in>")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(script_dir, sys.argv[1])

    try:
        if not os.path.isfile(file_name):
            print(f"File not found: {file_name}")
            sys.exit(1)

        data = parse_file(file_name)
        json_data = json.dumps(data, indent=4)
        #print(json_data)
    except ValueError as e:
        print(e)
        sys.exit(1)

    
    process_names = []
    arrival_times = []
    burst_times = []

    for process in data["processes"]:
        process_names.append(process["name"])
        arrival_times.append(process["arrival"])
        burst_times.append(process["burst"])

    if data["algorithm"]=="fcfs":
        fifo_scheduler(data["processcount"], process_names, data["runfor"], arrival_times, burst_times)


    processes = []
    for process in data["processes"]:
        processes.append(Process(process["name"], process["arrival"], process["burst"]))
        

    if data["algorithm"]=="sjf":
        preemptive_sjf(data["processcount"], data["runfor"], data["algorithm"], processes)
    

if __name__ == "__main__":
    main()