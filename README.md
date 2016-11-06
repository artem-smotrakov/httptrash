# httptrash
## Dumb HTTP1 fuzzer
`httptrash.py` is a mutation-based HTTP1 fuzzer. It takes an HTTP request, mutates it, and sends to an HTTP server. All test cases which the fuzzer generates are reproducible by specifying a number of test case with `--test` option.
### Usage
```
usage: httptrash.py [-h] [--verbose] [--port PORT] [--host HOST] [--seed SEED]
                 [--test TEST] [--ratio RATIO] [--request REQUEST]

optional arguments:
  -h, --help         show this help message and exit
  --verbose          more logs
  --port PORT        port number
  --host HOST        host name
  --seed SEED        seed for pseudo-random generator
  --test TEST        test range, it can be a number, or an interval
                     "start:end"
  --ratio RATIO      fuzzing ratio range, it can be a number, or an interval
                     "start:end"
  --request REQUEST  path to file with HTTP request to fuzz
  ```
### Examples

Use build-in HTTP request, generate 10 fuzzed HTTP requests, modify %5 of the original request, send requests to an HTTP server on port 55555  
```
./httptrash.py --port 55555 --ratio 0.05 --test 0:10
```

Repeat test case #5 from the command above
```
./httptrash.py --port 55555 --ratio 0.05 --test 5
```
