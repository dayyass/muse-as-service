import multiprocessing


def max_workers_and_threads():
    return multiprocessing.cpu_count() * 2 + 1


bind = "0.0.0.0:5000"
workers = max_workers_and_threads()
threads = max_workers_and_threads()
timeout = 0
