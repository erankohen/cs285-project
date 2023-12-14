import os 
import re
import json
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.pie import * 
import tot.methods.bfs as bfs
import numpy as np 
from src.codenet_eval.sandbox import run_code_on_inputs
import glob

class PieTask(Task):
    ideas = [
        '',
        'using mathematical reasoning where you use critical thinking and logical thinking to solve mathematical problems', # make these more verbose
        # 'using numpy vectorizations',
        # 'using fancy indexing',
        # 'using more efficient packages',
        # 'using built-in functions',
        # 'using bitwise operations',
        'using creative solutions where you rethink the structure of the code',
        # 'using list comprehensions'
    ]
    
    def __init__(self, file='../../self-refine/data/tasks/pie/codenet-python-test-1k.jsonl', run_count=4, test_count=1):
        with open(file) as f:
            data = f.readlines()
        self.data = []
        for line in data: 
            self.data.append(json.loads(line)) 
        self.steps = 4
        self.stops = ['### END ###'] * self.steps
        self.value_cache = {}

        self.runtime_cache = {}
        self.run_count = run_count
        self.test_count = test_count
        self.ground_truth_cache = {}

        self.code_path = './temp.py'
        self.inputs_outputs_basepath = "../../self-refine/data/codenet/generated_test_cases"

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int) -> str:
        return self.data[idx]['input']

    def test_output(self, idx: int, outputs: str, method: str):
        # check pie eval
        slow_code = self.get_input(idx)
        if method == "value":
            rs = [bfs.get_value(self, slow_code, output, 2, cache_value=True) for output in outputs]
        else: 
            rs = bfs.get_votes(self, slow_code, outputs, 3)
        return [{'r': r} for r in rs]
        
    @staticmethod 
    def standard_prompt_wrap(x: str, y:str, idea_idx:int) -> str:
        return standard_prompt.format(input=y if y else x, idea=PieTask.ideas[idea_idx])
        
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        return value_prompt.format(slow_code=x, improved_code=y)

    @staticmethod
    def vote_prompt_wrap(x: str, ys: list) -> str:
        options = ''
        for i, y in enumerate(ys, 1):
            # y = y.replace('Plan:\n', '')
            # TODO: truncate the plan part?
            options += f'Choice {i}:\n```\n{y}\n```\n'
        prompt = vote_prompt.format(slow_code=x, improved_versions=options)
        return prompt
    
    @staticmethod
    def vote_outputs_unwrap(vote_outputs: list, n_candidates: int) -> list:
        vote_results = [0] * n_candidates
        for vote_output in vote_outputs:
            pattern = r".*best choice is .*(\d+).*"
            match = re.match(pattern, vote_output, re.DOTALL)
            if match:
                vote = int(match.groups()[0]) - 1
                if vote in range(n_candidates):
                    vote_results[vote] += 1
            else:
                print(f'vote no match: {[vote_output]}')
        return vote_results
    
    
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
        match = re.findall(pattern, sample, re.DOTALL)
        if match: 
            if match[-1][:7] == "python\n": 
                return match[-1][7:]
            return match[-1]
        else:
            return ""
    
    def get_ground_truth_values(self, idx, x, ys):
        if x in self.runtime_cache:
            x_time = self.runtime_cache[x]
        else:
            x_time = self.run(idx, x)
            # assert x_time != float('inf')

        y_times = []
        for y in ys:
            if y in self.runtime_cache:
                y_times.append(self.runtime_cache[y])
            else:
                y_times.append(self.run(idx, y))
        
        if x_time == float('inf'):
            return list(- np.array(y_times))
        return list((x_time - np.array(y_times)) / x_time)
        
        

    def run(self, idx:int, code: str): 
        problem_id = self.data[idx]['problem_id']
        problem_path = f'{self.inputs_outputs_basepath}/{problem_id}'

        ground_truths = []
        if idx in self.ground_truth_cache:
            ground_truths = self.ground_truth_cache[idx]
        else:
            num_test_cases = len(
                glob.glob(f"{self.inputs_outputs_basepath}/{problem_id}/output*.txt")
            )
            assert (
                num_test_cases > 0
            ), f"{self.inputs_outputs_basepath}/{problem_id} has no ground truth files!"
            for i in range(num_test_cases):
                with open(f"{problem_path}/output.{i}.txt") as f:
                    ground_truths.append(f.read().strip() + "\n")
            self.ground_truth_cache[idx] = ground_truths
        
        with open(self.code_path, 'w+') as f:
            f.write(code)

        # import pdb; pdb.set_trace()
        avg_time, std_time, avg_acc, stats = run_code_on_inputs(
            language='python',
            code_path=self.code_path,
            ground_truths=ground_truths,
            unit_test_data_basepath=problem_path,
            num_runs_per_test_case=self.run_count,
            ignore_first_k=0,
            max_seconds_per_run=20,
            cpu_number=0,
            return_if_acc_below=1.0,
            num_test_cases=self.test_count
        )

        return avg_time * (float('inf') ** (not avg_acc))
