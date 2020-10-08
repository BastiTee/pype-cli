# -*- coding: utf-8 -*-
"""Internal helper to benchmark initialization process."""

from os import environ
from sys import stderr
from time import time

ENV_BENCHMARK_INIT = 'PYPE_BENCHMARK_INIT'


class Benchmark():
    """Benchmark context."""

    def __init__(self, key):  # noqa: D107
        self.active = self.__is_active()
        if not self.active:
            return
        self.key = key
        pass

    def __enter__(self):  # noqa: D105
        if not self.active:
            return
        self.start_time = time()

    def __exit__(self, type_s, value, traceback):  # noqa: D105
        if not self.active:
            return
        self.end_time = time()
        self.elapsed_ms = round(
            (self.end_time - self.start_time) * 1000, 5)
        print(f'{self.key} | {self.elapsed_ms} ms', file=stderr)

    @staticmethod
    def __is_active():
        return int(environ.get(ENV_BENCHMARK_INIT, 0)) == 1

    @staticmethod
    def print_info(message):
        """Print benchmark information."""
        if not Benchmark.__is_active():
            return
        print('- ' + message, file=stderr)
