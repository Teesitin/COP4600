from datetime import datetime
# Format the current date and time as a string (e.g., '2023-01-30_23-59-59')
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Simulate data generation
daobdfojnhbdrtfnobdftgoimnfxtnfh


jmyrtdryjtjtypjymyj

tyj
jmyrtdryjtjtypjymyjjdty
jmyrtdryjtjtypjymyjjyrtjdy
jdtyk
djty
jmyrtdryjtjtypjymyjjdytyjdt,mophjtrm,raiserth
jmyrtdryjtjtypjymyjr
th
jrht

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
