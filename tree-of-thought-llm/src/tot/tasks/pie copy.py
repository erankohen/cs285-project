import os 
import re
import json
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.pie import * 


class PieTask(Task):
    def __init__(self, file='../../self-refine/data/tasks/pie/codenet-python-test-1k.jsonl'):
        with open(file) as f:
            data = f.readlines()
        self.data = []
        for line in data: 
            self.data.append(json.loads(line)) 
        self.steps = 3
        self.stops = ['### END ###'] * self.steps
        self.value_cache = {}

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int) -> str:
        return self.data[idx]['input']

    def test_output(self, idx: int, output: str):
        # check pie eval
        slow_code = self.get_input(idx)

        yaml_content = '''
inputs_outputs_basepath: "../self-refine/data/codenet"
reference_file_path: "../self-refine/data/tasks/pie/codenet-python-test-1k.jsonl"
num_problems_to_evaluate: -1
num_trials: 4
ignore_first_k: 0
max_time_per_run: 10
temp_dir: null
model_generated_potentially_faster_code_col: "fast_code"
slow_code_col: "input"
reference_code_col: "target"
is_prompt_based: false
language: python
return_if_acc_below: 1.0
# num_processes: 60
cpu_number: 0
model_generated_outputs_path: "../tree-of-thought-llm/temp.json"
output_report_file_path: "../tree-of-thought-llm/report.json"
'''
        
        json_content = {
            **self.data[idx],
            'slow_code': slow_code,
            'fast_code': output
        }
        with open('../temp.json', 'w+') as f:
            json.dump(json_content, f)
        
        os.system('bash run_pie_eval.sh')
        return 
        
    @staticmethod 
    def standard_prompt_wrap(x: str, y:str) -> str: 
        return standard_prompt.format(input=y if y else x)
        
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        return value_prompt.format(slow_code=x, improved_code=y)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        pattern = r".*efficiency improvement fraction is (\d+\.?\d*).*"
        scores = []
        for out in value_outputs:
            match = re.match(pattern, out, re.DOTALL)
            if match:
                score = float(match.groups()[0])
                scores.append(score)
            else: 
                continue
        return (sum(scores)/len(scores)) if scores else float('-inf')
    
    @staticmethod
    def standard_prompt_unwrap(input: str, sample: str) -> str:
        pattern = r"```(.*)```"
        match = re.findall(pattern, sample, re.DOTALL)[-1]
        return match