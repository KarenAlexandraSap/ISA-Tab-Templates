from isatools import isatab

isa_tab_directory = "/home/karen/CFM_ISA/ISA-Tab-Templates/metadata/MTBLS4082"

try:
    investigation = isatab.load(isa_tab_directory)
    print("Investigation loaded:", investigation)
except Exception as e:
    print("Error loading ISA-Tab:", e)
