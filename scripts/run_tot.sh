# run from scripts
cd ../tree-of-thought-llm/src
conda run -n tot python ../run.py --task pie --task_start_index 0 --task_end_index 50 --prompt_sample standard --backend gpt-3.5-turbo --method_generate sample --method_evaluate vote --get_gt --use_idea

# change method_evaluate

cd ../../pie-perf
conda run -n cs285proj python src/codenet_eval/run_eval.py --eval_config ../tree-of-thought-llm/perf.yaml 

cd ../self-refine
conda run -n cs285proj python src/pie/pie_eval.py --report_path ../tree-of-thought-llm/reports --output_path ../tree-of-thought-llm/reports 