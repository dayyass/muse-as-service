import multiprocessing


def max_workers_and_threads() -> int:
    """
    Compute recommended number of gunicorn workers and threads.
    https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads

    :return: recommended number of gunicorn workers and threads.
    :rtype: int
    """

    return multiprocessing.cpu_count() * 2 + 1


HOST = "0.0.0.0"
PORT = 5000


# GUNICORN OPTIONS

bind = f"{HOST}:{PORT}"  # The socket to bind
workers = (  # The number of worker processes for handling requests
    max_workers_and_threads()
)
threads = (  # The number of worker threads for handling requests
    max_workers_and_threads()
)
timeout = 0  # Workers silent for more than this many seconds are killed and restarted

# You can also add other gunicorn options
