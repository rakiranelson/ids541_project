import subprocess
import sys

"""
Runs full IDS 541 pipeline:
1. Data construction
2. Cleaning
3. EDA
4. Modeling
5. Analysis
6. Memo generation
"""

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
