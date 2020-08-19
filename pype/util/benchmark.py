"""Benchmark."""

from os import environ
from time import time

ENV_BENCHMARK_INIT = 'PYPE_BENCHMARK_INIT'


class Benchmark():
    def __init__(self, key=None):
        self.active = self.__is_active()
        if not self.active:
            return
        self.key = key
        pass

    def __enter__(self):
        if not self.active:
            return
        self.start_time = time()

    def __exit__(self, type_s, value, traceback):
        if not self.active:
            return
        self.end_time = time()
        self.elapsed_ms = round(
            (self.end_time - self.start_time) * 1000, 5)
        print(self.elapsed_ms)

    @staticmethod
    def __is_active():
        return int(environ.get(ENV_BENCHMARK_INIT, 0)) == 1

    @staticmethod
    def print_info(message):
        if not Benchmark.__is_active():
            return
        print(message)
