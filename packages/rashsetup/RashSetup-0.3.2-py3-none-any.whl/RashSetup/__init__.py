import os
import json
import queue
import shutil
import threading
import sys
import time
import gc
import pathlib
import subprocess
import urllib.request
import concurrent.futures
import scrapy.crawler
import twisted.internet.reactor
import logging
import logging.handlers

from .RashScrappers.RashScrappers.spiders import *

__all__ = [
    "JsonHandler",
    "TempHandler",
    "Launcher",
    "RepoSetup",
    "READMESetup",
    "ModuleCheckerSetup",
    "UpdateCheckerSetup",
    "LockOut",
    "LockErr"
]

URL = "https://github.com/RahulARanger/RashSetup"


class JsonHandler:
    def __init__(self, file=None):
        self.file = file

    def load(self):
        with open(self.file, 'r') as loaded:
            return json.load(loaded)

    def dump(self, store):
        with open(self.file, 'w') as loaded:
            return json.dump(store, loaded, indent=4)

    def __call__(self, raw: str):
        return json.loads(raw)

    def __str__(self):
        return self.file

    def parse_url(self, raw_link):
        with urllib.request.urlopen(raw_link) as raw:
            return self(raw.read())

    def close(self):
        os.remove(self.file)


class PipeFD:
    def __init__(self, callback=None):
        self.buffer = None
        self.store = None

        self.callback = callback

    def write(self, text):
        return self.callback(text) if self.callback else text

    def writelines(self, lines):
        if not self.callback:
            return lines

        self.callback("".join(lines))

    def fileno(self):
        return self.store.fileno()

    def flush(self):
        return self.store.flush()

    def close(self):
        pass


class LockErr(PipeFD):
    def __init__(self, callback):
        super().__init__(callback)

        self.store = sys.stderr
        self.buffer = sys.stderr.buffer

        sys.stderr = self

    def close(self):
        sys.stderr = self.store


class LockOut(PipeFD):
    def __init__(self, callback):
        super().__init__(callback)

        self.store = sys.stdout
        self.buffer = sys.stdout.buffer

        sys.stdout = self

    def close(self):
        sys.stdout = self.store


"""
LOCK SAUCE:
    GLOBAL LOCK:
    'e' - exited
    '1' - high state
    '' - low state

    MAX LOCK:
        '1' - someone tried to open
        'e' - close application [TODO]

    Rash is opened if it toggle s between high and low state for every second

"""


class Launcher:
    def __init__(self, pwd, manager: concurrent.futures.ThreadPoolExecutor):
        self.pwd = pathlib.Path(pwd)
        self.pwd = self.pwd.parent if self.pwd.is_file() else self.pwd

        if not self.pwd.exists():
            raise FileNotFoundError(self.pwd)

        self.global_mutex = self.pwd / "GLOBAL.lock"
        self.max_mutex = self.pwd / "MAX.lock"

        None if self.test() else self._notify()

        self.workers = threading.Lock(), threading.Lock()

        manager.submit(
            self.read_thread
        )

        manager.submit(
            self.write_thread
        )

        self.remainder = None

    def _notify(self):
        self.max_mutex.write_text("1")
        return sys.exit(0)

    def register(self):
        pass

    def test(self):
        if not self.global_mutex.exists():
            self.global_mutex.write_text("")
            return True

        test_1 = self.global_mutex.read_text()

        if test_1 == 'e':
            return True

        time.sleep(1)

        test_2 = self.global_mutex.read_text()

        time.sleep(0.1)

        test_3 = self.global_mutex.read_text()

        if test_1 == test_2 and test_3 == test_1:
            return True

        return False

    def read_thread(self):
        self.workers[0].acquire()

        while self.workers[0].locked():

            code = None if self.max_mutex.exists() else self.max_mutex.write_text("")
            code = code if code else self.max_mutex.read_text()

            result = None if code == '' else self.remainder(code == '1') if self.remainder else None

            if result:
                break

            time.sleep(1)

        self.max_mutex.write_text("")

    def write_thread(self):
        self.workers[1].acquire()

        toggle = False

        while self.workers[1].locked():
            None if self.global_mutex.exists() else self.global_mutex.write_text("")

            self.global_mutex.write_text("" if toggle else "1")
            toggle = not toggle

            time.sleep(1)

    def close(self):
        for _ in self.workers:
            _.release()


class QueueHandler(logging.handlers.QueueHandler):
    def __init__(self, queue):
        super().__init__(queue)

    def handle(self, record):
        # to make this pickleable
        # avoiding all lambda functions from scrapy logs

        modified = logging.LogRecord(
            record.name,
            record.levelno,
            record.pathname,
            record.lineno,
            record.getMessage(),
            args=(),
            exc_info=record.exc_info,
            func=record.funcName,
            sinfo=record.stack_info
        )

        return super().handle(modified)


class Setup:
    def __init__(self, pipe=None,  log_pipe: queue.Queue = None, url=None, start=False):
        self.utils = None
        self.cache = {}

        self.logger = logging.getLogger("") if log_pipe else None
        self.pipe = pipe

        self.callback = None

        self.complete_setup(log_pipe) if self.logger else None
        self.start(url) if start else None

    def pass_start(self, *args):
        pass

    def start(self, *args):
        pass

    def save(self):
        temp = JsonHandler(
            TempHandler()(suffix=".json")
        )

        self.pipe.saved = self.cache

        self.logger.info("Saving raw data into %s", temp.file)

    def close(self, *args):
        twisted.internet.reactor.callWhenRunning(
            twisted.internet.reactor.stop
        )

    def complete_setup(self, handler_queue):
        self.logger.addHandler(
            QueueHandler(handler_queue)
        )


class READMESetup(Setup):
    def pass_start(
            self, url, callback
    ):
        crawler = scrapy.crawler.CrawlerProcess()

        signal = crawler.crawl(
            ReadmeSpider, pipe=self.cache, url=url
        )

        signal.addCallback(callback, self.cache)

        return crawler

    def start(self, url):
        crawler = self.pass_start(
            url, self.close
        )

        crawler.start(True)

    def close(self):
        super().close()

        return self.save()


class ModuleCheckerSetup(Setup):

    def pass_start(self, url, callback):
        self.utils = callback
        crawler = scrapy.crawler.CrawlerProcess()

        signal = crawler.crawl(
            ModuleCheckerSpider, url=url, pipe=self.cache
        )

        signal.addCallback(self.fetch_readme)

        crawler.start(False)

    def start(self, url):
        self.pass_start(
            url, self.save
        )

    def fetch_readme(self, *args):
        self.validate()

        if "README.md" not in self.cache:
            self.cache["readme"] = {
                "failed": True,
                "exception": "No README.md found in given REPO",
                "result": ""
            }

            self.utils(self.cache) if self.utils else None
            return

        url = self.cache["README.md"]

        setup = READMESetup()

        setup.pass_start(url, self.handle_readme)

    def handle_readme(self, _, *args):
        self.logger.info("Fetched README file") if self.logger else None
        self.cache["readme"] = args[0]

        self.utils(self.cache) if self.utils else None

    def validate(self):
        self.cache["result"] = all(
            (
                "settings.json" in self.cache,
                "setup.py" in self.cache
            )
        )

        None if self.cache["result"] else self.utils(self.cache) if self.utils else None

    def save(self, *args):
        self.close()
        return super().save()


class RepoSetup(Setup):
    def __init__(self, pipe, logger, url):
        super().__init__(pipe, logger)

        self.module = url

        self.start()

    def start(self):
        setup = ModuleCheckerSetup()
        setup.pass_start(self.module, self.passed)

    def passed(self, cache):
        self.cache.update(cache)

        if not self.cache["result"]:
            return self.save_error(f"{self.module} is not a Proper Rash Module")

        self.parse_settings()

    def parse_settings(self):
        settings = JsonHandler().parse_url(self.cache["settings.json"])
        self.cache["settings"] = settings

        crawler = scrapy.crawler.CrawlerProcess()

        signal = crawler.crawl(
            RepoSpider, url=settings["hosted"], name=settings["name"], pipe=self.cache
        )

        signal.addCallback(self.install)

    def install(self, *args):
        current = self.cache["result"]

        setup = os.path.join(current, "setup.py")

        if not os.path.exists(setup):
            return self.save_error("Missing setup.py file in the given repo")

        subprocess.run([
            sys.executable, setup, "sdist", "bdist_wheel"
        ], cwd=current
        )

        # subprocess.run([
        #     sys.executable, "-m", "pip", "install", current
        # ])
        #

        shutil.rmtree(
            current
        )  # deleting the directory

        self.cache["result"] = ""
        self.cache["failed"] = False
        self.cache["exception"] = ""

        self.save()

    def save_error(self, exc):
        self.cache["result"] = ""
        self.cache["failed"] = True
        self.cache["exception"] = exc
        self.save()

    def save(self):
        self.close()
        super().save()


class UpdateCheckerSetup(Setup):
    def __init__(self, pipe, logger, *modules):
        super().__init__(pipe, logger)

        self.start(modules)

    def start(self, modules):
        crawler = scrapy.crawler.CrawlerProcess()

        for module in modules:
            crawler.crawl(
                SettingsSpider, url=modules[module], pipe=self.cache, name=module
            )

        crawler.join().addCallback(self.save)
        crawler.start()

    def save(self):
        for module in self.cache:
            status, result = self.cache[module]

            if not status:
                continue

            try:
                self.cache[module] = JsonHandler().parse_url(self.cache[module])["version"]
            except Exception as error:
                self.cache[module] = False, str(error)

        super().save()


class UninstallSetup(Setup):
    pass


gc.collect()
