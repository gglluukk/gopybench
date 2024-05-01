#!/usr/bin/python3

import concurrent.futures
import multiprocessing 
import sys
import time
import threading

# define persons_num at least equal to 1,000,000 * number_of_cpu_cores
persons_num = 4000000


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <class_name> [lib|libc]".format(sys.argv[0]))
        sys.exit(1)
    class_name = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == 'libc':
        from libc import create_persons
    else:
        from lib import create_persons

    proc_num = multiprocessing.cpu_count()
  
    print(f"*** {class_name} object creation: single thread")
    start_time = time.time()
    create_persons(class_name, persons_num)
    print(f"* Total time: {time.time() - start_time:.2f} seconds\n")

    print(f"*** {class_name} object creation: {proc_num} threads")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=proc_num) as ex:
        futures = [ex.submit(create_persons, class_name, 
                                    int(persons_num / proc_num)) 
                   for _ in range(proc_num)]
        concurrent.futures.wait(futures)
    print(f"* Total time: {time.time() - start_time:.2f} seconds\n")

    print(f"*** {class_name} object creation: {proc_num} processes")
    start_time = time.time()
    processes = []
    for _ in range(proc_num):
        p = multiprocessing.Process(target=create_persons, 
                                    args=(class_name, persons_num // proc_num))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print(f"* Total time: {time.time() - start_time:.2f} seconds\n")

