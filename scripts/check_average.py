import json

all_data = None
with open("../self-refine/data/tasks/pie/codenet-python-test-1k.jsonl") as f:
    all_data = [json.loads(line) for line in f]

# data_100 = None
# with open("../self-refine/data/tasks/pie/random_100.jsonl") as f:
#     data_100 = [json.loads(line) for line in f]

# avg_100 = sum([d["cpu_time_v1"] for d in data_100]) / 100
# print(avg_100)

print(sum([d["cpu_time_v1"] for d in all_data[-100:]]) / (100))
all_avg = sum([d["cpu_time_v1"] for d in all_data]) / len(all_data)
print(all_avg)
