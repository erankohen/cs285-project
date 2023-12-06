import time
import numpy as np 
import os

slow_code = '''
import numpy as np
A = np.arange(1<<27,dtype=np.int32)


a,b = map(int,input().split())
if (a-b) % 2 == 0:
  print((a+b)//2)
else:
  print('IMPOSSIBLE')
'''

fast_code = '''
import sys
read = sys.stdin.buffer.read
readline = sys.stdin.buffer.readline
readlines = sys.stdin.buffer.readlines

A,B = map(int,read().split())

q,r = divmod(A+B,2)

if r == 1:
    print('IMPOSSIBLE')
else:
    print(q)
'''

inputs = [
    "2 20",
    "20 50",
    "200 301"
]

def prep_code(code):
    with open("./temp.py", 'w+') as f:
        f.write(code)

def run_code(inputs):
    for i in inputs:
        os.system(f'echo "{i}" | python ./temp.py')

slow_times = []
fast_times = []
for _ in range(15):
    prep_code(slow_code)
    start = time.time()
    run_code(inputs)
    end = time.time()
    slow_times.append(end - start)
    
    prep_code(fast_code)
    start = time.time()
    run_code(inputs)
    end = time.time()
    fast_times.append(end - start)

print(np.average((np.array(slow_times) - np.array(fast_times))/np.array(slow_times)) * 100)