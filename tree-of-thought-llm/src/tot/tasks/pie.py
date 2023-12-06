import os
import json
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.pie import * 


class PieTask(Task):
    def __init__(self, file='self-refine/data/tasks/pie/codenet-python-test-1k.jsonl'):
        with open(file) as f:
            data = f.readlines()
        self.data = []
        for line in data: 
            self.data.append(json.loads(line)) 

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int) -> str:
        return self.data[idx]

    def test_output(self, idx: int, output: str):
        # check pie eval
				# pass
        
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        pass
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        pass