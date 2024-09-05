import sys
import threading
import traceback
from os import environ as env

bind = '0.0.0.0:8000'
backlog = 2047

preload_app = True

workers = int(env.get('GUNICORN_WORKERS_NUM', '5'))
worker_class = 'sync'
worker_connections = 1000
timeout = 25
keepalive = 2
max_requests = 300000
max_requests_jitter = 10000

daemon = False
pidfile = None
umask = 0
group = 'www-data'
user = 'www-data'
tmp_upload_dir = None

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = '-'
errorlog = '-'
loglevel = 'info'

proc_name = 'django'

limit_request_line = 4096
limit_request_fields = 80
limit_request_field_size = 16536


def on_starting(server):
    server.log.info('Server starting...')


def on_reload(server):
    server.log.info('Server reloading...')


def post_fork(server, worker):
    server.log.info('Worker spawned (pid: %s)', worker.pid)


def pre_fork(server, worker):
    server.log.info('Worker spawning (pid: %s)', worker.pid)


def pre_exec(server):
    server.log.info('Forked child, re-executing.')


def when_ready(server):
    server.log.info('Server is ready. Spawning workers')


def worker_int(worker):
    worker.log.info('worker received INT or QUIT signal')

    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for thread_id, stack in sys._current_frames().items():  # noqa: SLF001
        code.append('\n# Thread: %s(%d)' % (id2name.get(thread_id, ''), thread_id))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append('  %s' % (line.strip()))

    worker.log.debug('\n'.join(code))


def worker_abort(worker):
    worker.log.info('worker received SIGABRT signal')


def get_all_attr(obj, worker):
    for attr in obj.dict.items():
        worker.log.info(attr)


def get_item(headers: list, val: str):
    for key, value in headers:
        if key == val:
            return value


REMOTE_IP = 'REMOTE-IP'
X_REAL_IP = 'X-REAL-IP'
X_CORRELATION_ID = 'X-CORRELATION-ID'


def pre_request(worker, req):
    headers = req.headers

    client_ip = get_item(headers, X_REAL_IP) or get_item(headers, REMOTE_IP)
    correlation_id = get_item(headers, X_CORRELATION_ID)

    worker.log.warning(
        f'REQUEST {req.method}, {req.path}, {client_ip}, {correlation_id}, {worker.pid}',
    )


def post_request(worker, req, environ, resp):
    headers = req.headers
    client_ip = get_item(headers, X_REAL_IP) or get_item(headers, REMOTE_IP)
    correlation_id = get_item(headers, X_CORRELATION_ID)
    worker.log.warning(
        f'RESPONSE {req.method}, {req.path}, {client_ip}, {correlation_id}, {worker.pid}, {resp.status}',
    )