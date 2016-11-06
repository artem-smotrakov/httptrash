#!/usr/bin/python

import textwrap
import random

verbose_flag = False

def verbose(*args):
    if verbose_flag:
        if len(args) == 0:
            return
        elif len(args) == 1:
            print(args[0])
        elif len(args) == 2:
            verbose_with_prefix(args[0], args[1])
        else:
            verbose_with_indent(args[0], args[1], args[2:])

def print_with_prefix(prefix, message):
    print('[{0:s}] {1}'.format(prefix, message))

def verbose_with_prefix(prefix, message):
    if verbose_flag:
        print_with_prefix(prefix, message)

def print_with_indent(prefix, first_message, other_messages):
    formatted_prefix = '[{0:s}] '.format(prefix)
    print('{0:s}{1}'.format(formatted_prefix, first_message))
    if len(other_messages) > 0:
        indent = ' ' * len(formatted_prefix)
        wrapper = textwrap.TextWrapper(
            initial_indent=indent, subsequent_indent=indent, width=70)
        for message in other_messages:
            print(wrapper.fill(message))

def verbose_with_indent(prefix, first_message, other_messages):
    if verbose_flag:
        print_with_indent(prefix, first_message, other_messages)

def bytes2hex(data):
    return ' '.join('{:02x}'.format(b) for b in data)

class DumbByteArrayFuzzer:

    def __init__(self, data, seed = 1, min_ratio = 0.01, max_ratio = 0.05,
                 start_test = 0, ignored_bytes = ()):
        # TODO: check if parameters are valid
        self.start_test = start_test
        self.test = start_test
        self.data = data
        self.seed = seed
        self.min_bytes = int(float(min_ratio) * int(len(data)));
        self.max_bytes = int(float(max_ratio) * int(len(data)));
        self.verbose('min bytes to change: {0:d}'.format(self.min_bytes))
        self.verbose('max bytes to change: {0:d}'.format(self.max_bytes))
        self.ignored_bytes = ignored_bytes
        self.reset()

    def set_test(self, test):
        self.test = test

    def reset(self):
        self.test = self.start_test
        self.random = random.Random()
        self.random.seed(self.seed)
        self.random_n = random.Random()
        self.random_position = random.Random()
        self.random_byte = random.Random()

    def next(self):
        fuzzed = self.data[:]
        seed = self.random.random() + self.test
        if self.min_bytes == self.max_bytes:
            n = self.min_bytes
        else:
            self.random_n.seed(seed)
            n = self.random_n.randrange(self.min_bytes, self.max_bytes)
        self.random_position.seed(seed)
        self.random_byte.seed(seed)
        i = 0
        while (i < n):
            pos = self.random_position.randint(0, len(fuzzed) - 1)
            if self.isignored(fuzzed[pos]):
                continue
            b = self.random_byte.randint(0, 255)
            fuzzed[pos] = b
            i += 1
        self.test += 1
        return fuzzed

    def isignored(self, symbol):
        return symbol in self.ignored_bytes

    def verbose(self, message):
        verbose(DumbByteArrayFuzzer.__name__, message)

class DumbAsciiStringFuzzer:

    def __init__(self, string, seed = 1, min_ratio = 0.01, max_ratio = 0.05,
                 start_test = 0, ignored_symbols = ()):
        self.data = bytearray(string, 'ascii', 'ignore')
        self.ignored_bytes = ignored_symbols
        self.byte_array_fuzzer = DumbByteArrayFuzzer(
                self.data, seed, min_ratio, max_ratio, start_test, self.ignored_bytes)

    def set_test(self, test):
        self.byte_array_fuzzer.set_test(test)

    def reset(self):
        self.byte_array_fuzzer.reset()

    def next(self):
        return self.byte_array_fuzzer.next()
