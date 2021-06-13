import multiprocessing


def max_workers_and_threads() -> int:
    """
    Compute recommended number of gunicorn workers and threads.
    https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads

    :return: recommended number of gunicorn workers and threads.
    :rtype: int
    """

    return multiprocessing.cpu_count() * 2 + 1


bind = "0.0.0.0:5000"
workers = max_workers_and_threads()
threads = max_workers_and_threads()
timeout = 0
