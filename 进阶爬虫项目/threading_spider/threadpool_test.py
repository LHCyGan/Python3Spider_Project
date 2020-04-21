#1. twitter Timeline
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, as_completed
import time


def sleep_task(sleep_time, name):
    print("sleep {} s".format(sleep_time))
    time.sleep(sleep_time)
    print("end")
    return "bobby"


executor = ThreadPoolExecutor(max_workers=2)
task1 = executor.submit(sleep_task, 2, "bobby")
task2 = executor.submit(sleep_task, 3, "bobby")
task3 = executor.submit(sleep_task, 3, "bobby")
all_task = [task1, task2, task3]
for task in as_completed(all_task):
    print(task.result())
# wait([task1, task2, task3], return_when=ALL_COMPLETED)
print("main end")



