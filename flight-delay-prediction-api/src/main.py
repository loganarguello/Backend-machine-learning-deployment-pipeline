import subprocess
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

print("Running import and formatting...")
subprocess.run(["python3", str(SRC / "import_format.py")], check=True)

print("Running cleaning and filtering...")
subprocess.run(["python3", str(SRC / "clean_data.py")], check=True)

print("Running model training...")
model_env = os.environ.copy()
model_env.pop("MLFLOW_RUN_ID", None)

subprocess.run(["python3", str(SRC / "train_model.py")], check=True, env=model_env)

print("Pipeline completed.")