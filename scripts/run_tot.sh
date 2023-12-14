# run from scripts
cd ../tree-of-thought-llm/src
conda run -n cs285-tot python ../run.py --task pie --task_start_index 0 --task_end_index 100 --prompt_sample standard --backend gpt-3.5-turbo-1106 --method_generate sample --method_evaluate gt

# change method_evaluate

cd ../../pie-perf
conda run -n cs285-project python src/codenet_eval/run_eval.py --eval_config ../tree-of-thought-llm/perf.yaml 

cd ../self-refine
conda run -n cs285-project python src/pie/pie_eval.py --report_path ../tree-of-thought-llm/reports --output_path ../tree-of-thought-llm/task5.2_reports 