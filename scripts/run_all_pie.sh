echo "RUNNING SELF-REFINE"
python src/pie/run.py --slow_programs_file data/tasks/pie/test_file.jsonl  --max_attempts 6 --outfile data/tasks/pie/output --feedback_type rich

echo "PREPPING FOR PIE"
python src/pie/prep_for_pie_eval.py --model gpt-3.5-turbo --input_file data/tasks/pie/output.fb_rich.temp_0.0.engine_gpt-3.5-turbo.jsonl --base_output_path "data/tasks/pie/" --num_attempts 6

cd ../pie-perf

echo "RUNNING RUN_EVAL IN PIE"
for num in $(seq 0 5); do
python src/codenet_eval/run_eval.py --eval_config ../self-refine/data/tasks/pie/pie$num.yaml
done

cd ../self-refine

echo "RUNNING PIE_EVAL"
python src/pie/pie_eval.py --report_path data/tasks/pie/baseline_out
