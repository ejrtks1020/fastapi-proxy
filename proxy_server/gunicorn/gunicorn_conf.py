bind = "0.0.0.0:8080"
timeout = 600
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"

BASE_DIR = "/app/src"
chdir = BASE_DIR
