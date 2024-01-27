# Amari Terry

import json
import os
import sys

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
    

if __name__ == "__main__":
    main()
