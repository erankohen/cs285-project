import json
import os 

all_data = {}
with open("self-refine/data/tasks/pie/codenet-python-test-1k.jsonl") as f:
    all_data = {json.loads(line)['submission_id_v0']: json.loads(line) for line in f}

print(os.system("ls ~/Downloads/report_more_trials2.csv"))
speedups = {f'{i}': [] for i in range(4)}
spedup = set()
with open('/Users/joyliu/Downloads/report_more_trials2.csv') as f: 
		first = True
		lines = [line for line in f][1:]
		for line in lines[::-1]: 
				# if first: 
				# 	first = False
				# 	continue 
				run = line.split(',')[-1][0]
				submission_id = line.split(',')[1]
				if submission_id in spedup: 
					continue
				improvement = all_data[submission_id]['improvement_frac']
				speedups[run].append(improvement)
				spedup.add(submission_id)
        
print(speedups)