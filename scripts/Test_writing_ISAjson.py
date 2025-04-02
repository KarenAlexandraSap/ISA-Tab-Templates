import json
from isatools import isatab

isa_tab_directory = "/home/karen/CFM_ISA/ISA-Tab-Templates/metadata/MTBLS4082"
output_json_path = "/home/karen/CFM_ISA/mtbls-validation/my_json_output/MTBLS4082/test_isa.json"

# Load ISA-Tab
investigation = isatab.load(isa_tab_directory)

# Convert and save manually
try:
    with open(output_json_path, "w") as output_file:
        json.dump(investigation.to_dict(), output_file, indent=4)
    print(f"Successfully saved JSON to {output_json_path}")
except Exception as e:
    print(f"Error saving JSON: {e}")
