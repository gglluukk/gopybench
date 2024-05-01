# gopybench: Memory Usage and Performance For Object Creation: Go vs Python 

`gopybench` contains implementations in both Go and Python, designed to assess memory usage and performance across the entire lifecycle of object creation, initialization, and utilization.

## Sample Object
All the tests are performed on sample object `Person` with:

- members:
  - `strings`: `First Name` and `Last Name`,
  - `integer`: `Age`
- methods:
  - `Get Full Name`, returning string where First and Last Names merged,
  - `Increase Age`, where Age is increased by 1

## Go Implementation

[sample.go](sample.go) implements a Go program that iteratively creates instances of a `Person` struct, including associated methods, while monitoring memory allocation and timing with following approaches:
- single thread
- multiple threads, where the number of threads equals the number of cores


## Python Implementation

Python program [sample.py](sample.py) with [lib.py](lib.py) implements a logic that achieves the same task as the Go implementation using the following approaches:
- object creation via:
  - default manner: `Person` in `bench.sh` output below
  - [\_\_slots\_\_](https://wiki.python.org/moin/UsingSlots) enabled: `PersonSlots`
  - `dataobject` from [recordclass](https://pypi.org/project/recordclass/): `PersonDataObject`
- execution with:
  - single thread/process
  - multiple threads
  - multiple processes
- with different interpreters:
  - `Python`, CPython 3.12
  - `Cython`, 3.0.10 with [libc.pyx](libc.pyx) converted from `lib.py` 
  - `Pypy`, 3.10.14


## [bench.sh](bench.sh) shorten output

```
=== GOLANG
golang: single thread 530.055568ms
golang: multiple threads 396.051268ms
=== PYTHON
Person object creation: single thread 5.23 seconds
Person object creation: 2 threads 5.22 seconds
Person object creation: 2 processes 2.53 seconds
PersonSlots object creation: single thread 4.61 seconds
PersonSlots object creation: 2 threads 4.60 seconds
PersonSlots object creation: 2 processes 2.20 seconds
PersonDataObject object creation: single thread 2.43 seconds
PersonDataObject object creation: 2 threads 2.41 seconds
PersonDataObject object creation: 2 processes 1.27 seconds
=== CYTHON
Person object creation: single thread 3.22 seconds
Person object creation: 2 threads 3.19 seconds
Person object creation: 2 processes 1.74 seconds
PersonSlots object creation: single thread 3.16 seconds
PersonSlots object creation: 2 threads 3.26 seconds
PersonSlots object creation: 2 processes 1.73 seconds
PersonDataObject object creation: single thread 3.20 seconds
PersonDataObject object creation: 2 threads 3.26 seconds
PersonDataObject object creation: 2 processes 1.65 seconds
=== PYPY
Person object creation: single thread 1.61 seconds
Person object creation: 2 threads 1.47 seconds
Person object creation: 2 processes 1.67 seconds
PersonSlots object creation: single thread 1.60 seconds
PersonSlots object creation: 2 threads 1.45 seconds
PersonSlots object creation: 2 processes 1.67 seconds
PersonDataObject object creation: single thread 1.59 seconds
PersonDataObject object creation: 2 threads 1.43 seconds
PersonDataObject object creation: 2 processes 1.66 seconds
```
- see [bench.log](bench.log) for full output


### Conclusion

Based on the benchmark results comparing memory usage and performance for object creation between Go and Python implementations, several key findings emerged:

- **Go**:
  - multiple threads implementation showcased the best timing, completing in 0.396 seconds.

- **Python**:
  - `dataobject` from the `recordclass` library with multiple processes achieved the best timing for default `Python` interpreter, completing in 1.27 seconds,
  - `__slots__` and `dataobjects` implementations didn't significantly impact timing for both `Cython` and `Pypy`,
  - `Cython` with multi-process implementations were found to be more efficient than its other approaches,
  - `Pypy` with multithreaded implementation showed better performance than its other approaches.

These results underscore the efficiency of `Go`'s concurrency model, particularly in multi-threaded scenarios. However, `Python` demonstrates competitive performance and can be further optimized through strategic techniques such as leveraging multiple processes with `dataobject` from `recordclass` for default interpreter. 


