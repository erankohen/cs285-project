Tree of Code, CS285 Final Project
Joy Liu, Eran Kohen Behar

To run our Tree-of-Thought implementation for code optimization, please see `scripts/run_tot.sh`. It will run ToT, evaluate all final code outputs, and generate a report on the results. This script uses two different conda environments, `cs285-project` and `cs285-tot`. `cs285-project` should contain all required packages for self-refine, pie-perf, and prompt-lib. `cs285-tot` should contain all required packages for tree-of-thought-llm, `joblib`, and `pandarallel` to run the oracle evaluation method that is based on pie-perf.

To reproduce self-refine results, see `scripts/run_all_pie.sh`. It will run self-refine, format the results to be compatible with the evaluation scripts, evaluate results, and generate a report.

Self refine prompts are in `self-refine/data/prompt/pie`.

Our ToT prompts are in `tree-of-thought-llm/src/tot/prompts/pie.py`. For a better understanding of how each prompt is used in the code, please see `tree-of-thought-llm/src/tot/tasks/pie.py`.