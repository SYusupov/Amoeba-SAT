import subprocess
import time

for i in range(21,250):
    starttime = time.time()
    s = subprocess.call(['python','trials_code.py','{}'.format(i*4-1),'{}'.format(i*4+3)])
    print("It took {} seconds".format(time.time() - starttime))
