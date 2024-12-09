output_dir=$(date "+%Y-%m-%d-%H-%M-%S")
python3 main.py --directory outputs/$output_dir
python3 testing.py --directory outputs/$output_dir
python3 scripts/average_outputs.py --directory outputs/$output_dir