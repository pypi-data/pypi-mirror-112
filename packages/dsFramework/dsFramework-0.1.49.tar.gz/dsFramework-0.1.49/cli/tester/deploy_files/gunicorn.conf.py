import multiprocessing
# bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
# timeout = 60
# graceful-timeout = 60
