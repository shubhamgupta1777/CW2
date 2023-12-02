import pandas as p

logs = p.read_json('./Files/sample_100k_lines.json')
print(logs['visitor_country'])

