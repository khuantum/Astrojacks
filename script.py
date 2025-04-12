import subprocess

scripts = [
    "load_training_data.py",
    "train_model.py",
    "convert.py",
    "format.py",
    "run_inference.py"
]

def main():
    
    for script in scripts:
        print(f"Running: {script}")
        result = subprocess.run(["python", script])

        if result.returncode != 0:
            print(f"!     Failed to run: {script}     !")
            break
        else:
            print(f"        {script} complete          ")

if __name__ == "main":
    main()