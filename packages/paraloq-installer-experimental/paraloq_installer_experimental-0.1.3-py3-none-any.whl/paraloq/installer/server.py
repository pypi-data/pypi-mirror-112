import threading
import uvicorn
import contextlib
import time


class Server(uvicorn.Server):
    def __init__(self, **kwargs):
        super(Server, self).__init__(**kwargs)
        self.thread = threading.Thread(target=self.run)

    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        self.thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            self.thread.join()

    def stop(self):
        self.should_exit = True
        self.thread.join()
