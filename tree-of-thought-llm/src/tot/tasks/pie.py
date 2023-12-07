import os 
import re
import json
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.pie import * 
import tot.methods.bfs as bfs

class PieTask(Task):
    def __init__(self, file='../../self-refine/data/tasks/pie/codenet-python-test-1k.jsonl'):
        with open(file) as f:
            data = f.readlines()
        self.data = []
        for line in data: 
            self.data.append(json.loads(line)) 
        self.steps = 4
        self.stops = ['### END ###'] * self.steps
        self.value_cache = {}

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
    def standard_prompt_wrap(x: str, y:str) -> str: 
        return standard_prompt.format(input=y if y else x)
        
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
        match = re.findall(pattern, sample, re.DOTALL)[-1]
        return match
        
        