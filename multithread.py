#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread

from utils import log_it


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks, daemon=False):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = daemon
        self.start()

    def run(self):
        func, args, kargs = self.tasks.get()
        try:
            func(*args, **kargs)
        except Exception, e:
            log_it(e, 'multithread-worker')
        self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        log_it("ADD TASK", 'multithread-pool')
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        log_it("COMPLETION", 'multithread-pool')
        self.tasks.join()
