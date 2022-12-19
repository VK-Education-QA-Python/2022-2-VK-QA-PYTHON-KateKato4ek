import requests
import time

class Waiter:
    @staticmethod
    def wait_ready(host, port):
        started = False
        st = time.time()
        while time.time() - st <= 5:
            try:
                requests.get(f'http://{host}:{port}')
                started = True
                break
            except ConnectionError:
                pass

        if not started:
            raise RuntimeError('App did not started in 5s!')
