#!/usr/bin/python

import connection
import helper
from helper import DumbAsciiStringFuzzer

class DumbHTTP1RequestFuzzer:

    def __init__(self, host, port, request, seed = 1, min_ratio = 0.01, max_ratio = 0.05,
                 start_test = 0, end_test = 0, ignored_symbols = ('\r', '\n')):

        if (seed == 0):
            raise Exception('Seed cannot be zero')

        self.host = host
        self.port = port
        self.end_test = end_test
        self.start_test = start_test
        self.dumb_ascii_string_fuzzer = DumbAsciiStringFuzzer(
            request, seed, min_ratio, max_ratio, start_test, ignored_symbols)

    def reset(self):
        self.dumb_ascii_string_fuzzer.reset()

    def next(self):
        return self.dumb_ascii_string_fuzzer.next()

    def run(self):
        test = self.start_test
        self.info('started, test range {0:d}:{1:d}'
                  .format(self.start_test, self.end_test))
        while (test <= self.end_test):
            self.info('test {0:d}: send'.format(test))
            client = connection.Client(self.host, self.port)
            try:
                client.send(self.next())
                data = client.receive()
                self.info('test {0:d}: received: {1}'.format(test, data.decode('ascii', 'ignore').split('\n', 1)[0]))
            finally:
                client.close()
            test += 1

    def info(self, message):
        print("[{0}] {1}".format(DumbHTTP1RequestFuzzer.__name__, message))
