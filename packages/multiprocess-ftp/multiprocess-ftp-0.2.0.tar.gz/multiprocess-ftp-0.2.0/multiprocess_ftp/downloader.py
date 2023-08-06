"""Multiprocessing orchestrators for downloading files from FTP."""
import logging
import os
import queue
import threading
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager
from typing import Any

from multiprocess_ftp.better_queue import BetterQueue
from multiprocess_ftp.proxy import BetterProxy
from multiprocess_ftp.sources import FTPConnection

# The time in seconds to wait between checking work queues for completion.
WORKER_WAIT_INTERVAL = 2
CHUNK_SIZE_IN_BYTES = 1024 ** 2 * 10  # 10MB


class FTPDownloadDirectoryWorker(Process):
    """A process worker that enumerates directories and files."""

    def __init__(
        self,
        name: str,
        source_connection_class,
        download_queue: queue,
        walk_queue: queue,
        result_queue: queue,
    ):
        """Initialize the worker."""
        Process.__init__(self)
        self.name = str(name)
        self.download_queue = download_queue
        self.walk_queue = walk_queue
        self.result_queue = result_queue
        self.source_connection_class = source_connection_class

    def run(self):
        """Make the worker run."""
        while True:
            queue_item = self.walk_queue.get()
            if not queue_item:
                continue
            self.source, destination = queue_item
            self.subdirectory = self.source.pop("subdirectory")
            for root, dirs, files in self.walk_remote_directory():
                for item in dirs:
                    self.source["subdirectory"] = os.path.join(root, item)
                    self.walk_queue.put((self.source, destination))
                for file_name in files:
                    self.source["subdirectory"] = os.path.join(root, file_name)
                    self.download_queue.put((self.source, destination))
            self.walk_queue.task_done()

    def walk_remote_directory(self):
        """Walk remote directory and generate directory and files names."""
        logging.info(
            "Worker: %s, Walking directory %s.",
            self.name,
            self.subdirectory,
        )
        with self.source_connection_class(**self.source) as host:
            response = [
                (root, dirs, files)
                for root, dirs, files in host.walk(self.subdirectory, followlinks=True)
            ]
            logging.info(
                "Worker: %s, Finished walking directory %s.",
                self.name,
                self.subdirectory,
            )
            return response


class FTPDownloadTransferWorker(Process):
    """A Process worker that downloads files."""

    def __init__(
        self,
        name: str,
        source_connection_class,
        download_queue: queue,
        walk_queue: queue,
        result_queue: queue,
        max_workers: int = 10,
    ):
        """Initialize the worker."""
        Process.__init__(self)
        self.name = str(name)
        self.download_queue = download_queue
        self.walk_queue = walk_queue
        self.result_queue = result_queue
        self.source_connection_class = source_connection_class
        self.max_workers = max_workers

    def run(self):
        """Download a file."""
        while True:
            queue_item = self.download_queue.get()
            if not queue_item:
                continue
            self.source, destination = queue_item
            remote_path = self.source.pop("subdirectory")
            logging.info("Worker: %s, Extracting file %s.", self.name, remote_path)
            self.chunk_queue = queue.Queue()
            with self.source_connection_class(**self.source) as host:
                st_size = host.stat(remote_path).st_size
            for chunk in self.get_chunks(remote_path, st_size):
                self.chunk_queue.put((chunk, destination))
            with destination as upload:
                for _ in range(self.max_workers):
                    ChunkWorker(
                        self.source_connection_class,
                        self.chunk_queue,
                        self.source,
                        upload,
                        remote_path,
                    ).start()
                while not self.chunk_queue.empty():
                    part, etag = self.chunk_queue.get()
                    destination.finished_parts.append(
                        {"PartNumber": part, "ETag": etag}
                    )
                    self.chunk_queue.task_done()
                self.chunk_queue.join()
            logging.info(
                "Worker: %s, Finished extracting file %s.",
                self.name,
                remote_path,
            )
            self.result_queue.put(destination)
            self.download_queue.task_done()

    def get_chunks(self, file_name, st_size):
        chunks = []
        part = 1
        for i in range(0, st_size + 1, CHUNK_SIZE_IN_BYTES):
            chunks.append((file_name, part, (i, i + CHUNK_SIZE_IN_BYTES)))
            part += 1
        return chunks


class ChunkWorker(threading.Thread):
    def __init__(
        self,
        source_connection_class,
        chunk_queue: queue,
        creds,
        destination,
        remote_path,
    ):
        super().__init__()
        self.source_connection_class = source_connection_class
        self.chunk_queue = chunk_queue
        self.creds = creds
        self.destination = destination
        self.remote_path = remote_path

    def run(self):
        while True:
            queue_item = self.chunk_queue.get()
            if len(queue_item):
                remote_file, part, (start, end) = queue_item
            with self.source_connection_class(**self.creds) as host:
                with host.open(self.remote_path, "rb") as fp:
                    fp.seek(start, 0)
                    self.destination.put(part, fp.read(end - start))


class WorkerNumber:
    """A counter to keep track of how many workers are spun up."""

    def __init__(self, start: int = -1):
        self.counter = start

    def __next__(self):
        self.counter += 1
        return self.counter


class MultiProcessDownloader:
    """Orchestrator for parallel downloads."""

    WORKER_NUMBER = WorkerNumber()

    def __init__(
        self,
        source_connection_class: Any,
        worker_classes: Any,
        max_workers: int = 10,
    ):
        """Initialize the orchestrator."""
        self.worker_classes = worker_classes
        self.max_workers = max_workers
        self.source_connection_class = source_connection_class
        BaseManager.register("BetterQueue", BetterQueue, proxytype=BetterProxy)
        manager = BaseManager()
        manager.start()
        self.download_queue = manager.BetterQueue()
        self.walk_queue = manager.BetterQueue()
        self.result_queue = manager.BetterQueue()

    def queue_workers(self):
        """Initialize and start workers."""
        for worker_class in self.worker_classes:
            for _ in range(round(self.max_workers / len(self.worker_classes))):
                worker_num = next(self.WORKER_NUMBER)
                logging.info("Starting %s%d.", worker_class.__name__, worker_num)
                worker_class(
                    worker_class.__name__ + str(worker_num),
                    self.source_connection_class,
                    self.download_queue,
                    self.walk_queue,
                    self.result_queue,
                ).start()

    def load_queue(self, source, destination):
        """Put items in the queue for directory worker to process."""
        self.walk_queue.put((source, destination))

    def wait_workers(self):
        """Wait for queues to be processed."""
        while (
            not self.walk_queue.all_tasks_done()
            or not self.download_queue.all_tasks_done()
        ):
            time.sleep(WORKER_WAIT_INTERVAL)
        self.walk_queue.join()
        self.download_queue.join()
        result_paths = []
        for _ in range(self.result_queue.qsize()):
            result_paths.append(self.result_queue.get())
            self.result_queue.task_done()
        self.result_queue.join()
        return result_paths
