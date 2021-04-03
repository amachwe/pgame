
import subprocess
import sys
import pymongo
from matplotlib import pyplot as plt

SCRIPT = "game.py"

games_result = []
import time
run_id = str(time.time())
for i in range(0,50):
    try:
        res = subprocess.check_call(['python',SCRIPT, run_id],stdout=sys.stdout, stderr=subprocess.STDOUT)
        
    except subprocess.CalledProcessError as e:
        games_result.append(e.returncode)

print("Run ID:", run_id)


