# Modify lightburn files to comply with UCCNC controller
import re
import argparse
# Path to the original file
file_path = 'powerScale.gc'
# Create the parser
parser = argparse.ArgumentParser(description="Exported lightburn geode file to convert to UCCNC format")

# Add the positional argument
parser.add_argument('file', nargs='?', default=file_path)

# Parse the arguments
args = parser.parse_args()

# Now args.file is the file name given on the command line, or fileName if no file name was given
print(args.file)
file_path = args.file
# Read the original file content
with open(file_path, 'r') as file:
    content = file.readlines()

# Initialize variables for tracking the first occurrence and previous values
first_m3_replaced = False
previous_m10q_value = None
last_m5_encountered = False

# Initialize the modified content list
modified_content = []

# Process each line according to the rules
for line in content:
    # Rule 1: Change GRBL-M3 to GRBL
    if 'GRBL-M3' in line:
        line = line.replace('GRBL-M3', 'modified GRB-M3 to UCCNC')

    # Rule 2: Replace the first M3 with M3M11
    if 'M3' in line and not first_m3_replaced:
        line = line.replace('M3', 'M3M11', 1)
        first_m3_replaced = True

    # Rule 6: Replace S0 with M11 (implemented before Rule 3)
    line = line.replace('S0', 'M11')

    # Rule 3: Replace Sxxx with M10Qxxx wherever it appears in the line
    line = re.sub(r'S(\d{1,3})', lambda match: "M10Q" + match.group(1) if 0 <= int(match.group(1)) <= 255 else match.group(0), line)

    # Rule 4: Replace subsequent M3 with M10Qxxx
    if 'M3' in line and first_m3_replaced:
        if previous_m10q_value is not None:
            line = 'M10Q' + previous_m10q_value + '\n'

    # Rule 5: Replace M5 with M11, except the last M5
    if 'M5' in line and not last_m5_encountered:
        if 'M5' in content[content.index(line)+1:]:
            line = line.replace('M5', 'M11')
        else:
            last_m5_encountered = True

    # Add the modified line to the list
    modified_content.append(line) 

# Path for the modified file
modified_file_path = file_path.replace('.gc', '_uccnc.nc')

# Write the modified content to a new file
with open(modified_file_path, 'w') as file:
    file.writelines(modified_content)
