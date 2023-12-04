import pandas as p
import json
import time

start_time = time.time()

#logs = p.read_json('./Files/sample_100k_lines.json')
logs = p.read_json('./output_files/output_file.json')

print(logs['ts'])

end_time = time.time()
execution_time = end_time - start_time

print(f"Processing lines took {execution_time:.2f} seconds.")