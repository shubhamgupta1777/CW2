import pandas as p

logs = p.read_json('./sample_100k_lines.json')
print(logs['visitor_country'])

