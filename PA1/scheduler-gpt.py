# Amari Terry

import json
import os
import sys
import itertools

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_burst = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.finish_time = -1
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1
        self.has_arrived = False

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

    with open("output.out", "w") as output_file:

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


    # html code is edited chatgpt code
    html_output = open("output.html", "w")
    html_output.write("<html><body>")

    timeline = set()
    selected_processes = set()

    # manually added code that opens the .out file and executes instructions in block then closes
    with open("output.out", "w") as output_file:

        # manually added code to write output to a .out file
        output_file.write(str(process_count) + " processes\n")
        output_file.write("Using " + str(scheduling_algorithm))

        html_output.write("<p><font color = 'magenta'>" + str(process_count) + " processes" + "</font></p>")
        html_output.write("<p><font color 'teal'>" + "Using " + str(scheduling_algorithm) + "</font><p>")

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
                output_file.write("Invalid scheduling algorithm")
                html_output.write("<p><font color = 'red'>" + "Invalid scheduling algorithm" + "</font></p>")

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


        current_event = None

        output_file.write("\nTimeline:\n")
        html_output.write("<p><font>" + "\nTimeline:\n" + "</font></p>")

        for time, event, event_type in sorted(timeline, key=lambda x: (x[0], x[2])):
            if event_type == 'arrived':

                output_file.write("Time\t" + str(event.arrival_time) + " : " + str(event.process_id) + " arrived\n")
                html_output.write("<p><font color = 'blue'>" + "Time\t" + str(event.arrival_time) + " : " + str(event.process_id) + " arrived\n" + "</font></p>")

            elif event_type == 'selected':
                if event != current_event:
                    output_file.write("Time\t" + str(time) + " : " + str(event.process_id) + " selected (burst\t" + str(event.burst_time) + ") \n")
                    html_output.write("<p><font color = 'green'>" + "Time\t" + str(time) + " : " + str(event.process_id) + " selected (burst\t" + str(event.burst_time) + ") \n" + "</font></p>")

                    current_event = event
            elif event_type == 'finished':
                output_file.write("Time\t" + str(time) + " : " + str(event.process_id) + " finished\n")
                html_output.write("<p><font color = 'maroon'>" + "Time\t" + str(time) + " : " + str(event.process_id) + " finished\n" + "</font></p>")

            elif event_type == 'idle':
                output_file.write("Time\t" + str(time) + " : Idle\n" )
                html_output.write("<p><font color = 'red'>" + "Time\t" + str(time) + " : Idle\n" + "</font></p>")




        output_file.write("\nFinished at time " + str(current_time))
        html_output.write("<p><font color = 'orangered'>" + "\nFinished at time " + str(current_time) + "</font></p>")

        # Calculate and print statistics
        for i in range(process_count):
            # manually added conditional that checks current process finishes
            if selected_process.finish_time == 0 or selected_process.finish_time >= run_for:
                output_file.write(str(processes[i].process_id) + " did not finish\n")
                html_output.write("<p><font = 'crimson'>" + str(processes[i].process_id) + " did not finish\n")
            output_file.write("\n" + str(processes[i].process_id) + " wait\t" + str(waiting_time[i]) + " turnaround\t" + str(turnaround_time[i]) + " response\t" + str(response_time[i]))
            html_output.write("<p><font color = 'deeppink'>" + "\n" + str(processes[i].process_id) + " wait\t" + str(waiting_time[i]) + " turnaround\t" + str(turnaround_time[i]) + " response\t" + str(response_time[i]) + "</font></p>")

        html_output.write("</body></html>")
        html_output.close()




def round_robin(processes, quantum, run_for):
    output_lines = [""] # attempt at troubleshooting
    current_time = 0
    ready_queue = []  # Initialize ready queue with no processes
    completed_processes = []
    last_event_time = 0
    output_lines = []
    previous_process = None  # Track previously selected process
    quantum_remainder = 0 #added the quantum remainder
    current_process = None # added the current process

    output_lines.append(str(len(processes)) + " processes\n")
    output_lines.append("Using Round-Robin\n")
    output_lines.append("Quantum   " + str(quantum) + "\n\n")

    while current_time < run_for:
        # Check for arrival_times
        for process in processes:
            if process.arrival_time == current_time: # changed logicalparameter
                ready_queue.append(process)
                output_lines.append("Time " + str(current_time) + " : " + process.process_id + " arrived\n")

        if (not (current_process == None)): # changed logic to handle conditions
            if (current_process.remaining_burst == 0): # cont.

                output_lines.append("Time " + str(current_time) + " : " + current_process.process_id + " finished\n")
                completed_processes.append(current_process)
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.wait_time = current_process.turnaround_time - current_process.burst_time
                quantum_remainder = 0
                current_process = None

            elif (quantum_remainder == 0):
                ready_queue.append(current_process)

        # Select process to execute
        if ready_queue and quantum_remainder == 0: #changed logic for next block to ensure no clashing
            quantum_remainder = quantum
            current_process = ready_queue.pop(0)
            if (current_process.response_time == -1):
                current_process.response_time = current_time - current_process.arrival_time
            output_lines.append(
                "Time " + str(current_time) + " : " + current_process.process_id + " selected (burst_time " + str(
                    current_process.remaining_burst) + ")\n")
        elif (len(ready_queue) == 0 and quantum_remainder == 0):
            output_lines.append("Time " + str(current_time) + " : Idle\n")
            current_time += 1
            continue

        current_time += 1
        current_process.remaining_burst -= 1
        quantum_remainder -= 1

    output_lines.append("Finished at time   " + str(current_time) + "\n\n")

    # Output the completed processes with statistics

    for process in processes:
        if (process.turnaround_time > 0):
            output_lines.append(
                "Name: " + process.process_id + " - Wait Time: " + str(
                    process.wait_time) + " - Turnaround Time: " + str(
                    process.turnaround_time) + " - Response Time: " + str(
                    process.response_time) + "\n")

    for process in processes:
        if (process.turnaround_time == 0):
            output_lines.append(process.process_id + " did not finish\n")

    # Write output to file
    with open("output.out", "w") as output_file:
        for line in output_lines:
            output_file.write(line)
 #customized output
    colors = ["blue", "plum", "darkgreen", "indigo", "violet"]
    # Write output to HTML file
    with open("output.html", "w") as output_file:
        output_file.write("<html>\n<head>\n")
        output_file.write("<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"><link href=\"https://fonts.googleapis.com/css2?family=DotGothic16&display=swap\" rel=\"stylesheet\">")
        output_file.write("<style>\n")
        output_file.write("body { font-family: 'DotGothic16', arial, sans-serif; color: white; }\n")
        output_file.write("table, th, td {\nborder: 0px solid; float: center;}\ntable {\n width: 50%;\n}\n")
        output_file.write("</style>\n")
        output_file.write("</head>\n")
        output_file.write("<body>\n")

        output_file.write("<center><table style=\"background-color: black;\">\n")

        for line in output_lines:
            output_file.write("<tr><td>\n" + line + "</td></tr>\n")

        output_file.write("</table></center>\n</body>\n</html>")

    return completed_processes

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


    if data["algorithm"]=="rr":
        completed_processes = round_robin(processes, data['quantum'], data["runfor"])


if __name__ == "__main__":
    main()
