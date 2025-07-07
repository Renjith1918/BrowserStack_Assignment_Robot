import subprocess
import os
import json
import multiprocessing
import traceback

platforms = ["windows", "windows_edge", "macos", "android", "ios"]

def run_robot_test(platform):
    print(f"BrowserStack opening in {platform}...")
    output_dir = f"reports/logs_{platform}_{os.getenv('TIMESTAMP', 'run')}"
    os.makedirs(output_dir, exist_ok=True)
    env = os.environ.copy()
    env["PLATFORM"] = platform
    try:
        result = subprocess.run(
            ["robot", "--outputdir", output_dir, "./tests/run_parallel.robot"],
            env=env,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Test completed in {platform}...")
        else:
            print(f"❌ Test failed in {platform}...")
            print("--- STDOUT ---")
            print(result.stdout)
            print("--- STDERR ---")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Exception in {platform}: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    with multiprocessing.Pool(processes=5) as pool:
        pool.map(run_robot_test, platforms)
