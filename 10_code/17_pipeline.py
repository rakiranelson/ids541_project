import subprocess
import sys
import os

"""
Runs full IDS 541 pipeline:
1. Data construction
2. Cleaning
3. EDA
4. Modeling
5. Analysis
6. Memo generation
"""

# create directories
os.makedirs("20_intermediate_files", exist_ok=True)
os.makedirs("30_results", exist_ok=True)
os.makedirs("30_results/figures", exist_ok=True)
os.makedirs("40_docs", exist_ok=True)

scripts = [
    "10_code/11_make_df.py",
    "10_code/12_clean_data.py",
    "10_code/13_mh_provider_access_analysis.py",
    "10_code/14_model_training.py",
    "10_code/15_analysis.py",
    "10_code/16_generate_memo.py",
]

for script in scripts:
    print(f"Running {script}...")

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        sys.exit(1)

print("All steps completed successfully.")
