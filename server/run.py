from concurrent.futures import ThreadPoolExecutor
import subprocess

def run_server():
    subprocess.run(["python", "server.py"])

def run_main():
    subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_server)
        executor.submit(run_main)