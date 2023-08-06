# divsufsort-python

Python bindings for [libdivsufsort][1].

  [1]: https://github.com/y-256/libdivsufsort

## Getting Started

Install from pip.

```
pip install divsufsort
```

Import the module and call its `divsufsort` function.

```python
>>> from divsufsort import divsufsort
>>> divsufsort(b'The quick brown fox jumps over the lazy dog')
(9, 39, 15, 19, 34, 25, 3, 30, 0, 36, 10, 7, 40, 33, 2, 28, 16, 42, 32, 1, 6,
20, 8, 35, 22, 14, 41, 26, 12, 17, 23, 4, 29, 11, 24, 31, 5, 21, 27, 13, 18,
38, 37)
```

The function receives a bytes-like object, `b`, and returns the corresponding
suffix-array, that is a tuple of integers `r` such that `len(r) == len(b)` and
`b[r[i]:] < b[r[i+1]:]` for all `i`.
