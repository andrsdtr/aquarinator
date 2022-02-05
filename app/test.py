from multiprocessing.connection import wait
import time

timestamp1 = time.time()
print(timestamp1)
# Your code here
time.sleep(3)
timestamp2 = time.time()
print(timestamp2)
print("This took", (timestamp2 - timestamp1), "seconds")