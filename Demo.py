import time
import linecache as l
import os
import linecache

start_time = time.time()

# Input file path
input_file_path = './Files/sample_3m_lines.json'

# Output directory
output_directory = 'output_files/'

# Create the output directory if it doesn't exist

os.makedirs(output_directory, exist_ok=True)

# Initialize variables
line_count = 1
output_file = open(f'{output_directory}output_file.json', 'w')
# Read input file and write to different files
with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()
    print(len(lines))
    output_file.write('[\n')
    l = ''
    for i,line in enumerate(lines):
        l = line 
        if i != len(lines)-1:
            if '}' in line: 
                output_file.write(l.replace('}',"},"))
        else:
            output_file.write(l.replace('}',"}\n]"))

        line_count += 1
        
# Close the last output file
output_file.close()

print(f'Files written to {output_directory}')
end_time = time.time()
execution_time = end_time - start_time
print(f"Processing {line_count} lines took {execution_time:.2f} seconds.")