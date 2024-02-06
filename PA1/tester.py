from datetime import datetime
# Format the current date and time as a string (e.g., '2023-01-30_23-59-59')
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Simulate data generation
data = {
    "process_count": "5",
    "algorithm": "Round-Robin",
    "quantum": "3",
    "details": [
        {"time": "0", "event": "P1 arrived"},
        {"time": "0", "event": "P1 selected (burst 5)"},
        # Add more event data...
    ],
    "statistics": [
        {"process": "P1", "wait": "3", "turnaround": "8", "response": "0"},
        {"process": "P1", "wait": "3", "turnaround": "8", "response": "0"},
        {"process": "P1", "wait": "3", "turnaround": "8", "response": "0"},
        {"process": "P1", "wait": "3", "turnaround": "8", "response": "0"},
        {"process": "P1", "wait": "3", "turnaround": "8", "response": "0"},
        {"process": "P1", "wait": "3", "turnaround": "8", "response": "0"},
    ]
}

# Prepare details and statistics rows
details_rows = ''.join([f'<tr><td>Time {d["time"]}</td><td>{d["event"]}</td></tr>' for d in data["details"]])
statistics_rows = ''.join([f'<tr><td>{s["process"]}</td><td>{s["wait"]}</td><td>{s["turnaround"]}</td><td>{s["response"]}</td></tr>' for s in data["statistics"]])

# Fill the template
template_path = "template.html"
with open(template_path, 'r') as file:
    template = file.read()

template_filled = template.replace('{{ process_count }}', data["process_count"])
template_filled = template_filled.replace('{{ algorithm }}', data["algorithm"])
template_filled = template_filled.replace('{{ quantum }}', data["quantum"] if "quantum" in data else "N/A")
template_filled = template_filled.replace('{{ details_rows }}', details_rows)
template_filled = template_filled.replace('{{ statistics_rows }}', statistics_rows)

# Write the output to a new HTML file
output_path = f"outputs/output_{timestamp}.html"
with open(output_path, 'w') as file:
    file.write(template_filled)

print("HTML file has been generated.")
