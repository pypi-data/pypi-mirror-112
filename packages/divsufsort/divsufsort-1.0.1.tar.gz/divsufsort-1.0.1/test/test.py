from divsufsort import divsufsort
sa = divsufsort(b'The quick brown fox jumps over the lazy dog')
assert sa == (
    9, 39, 15, 19, 34, 25, 3, 30, 0, 36, 10, 7, 40, 33, 2, 28, 16, 42, 32, 1, 6,
    20, 8, 35, 22, 14, 41, 26, 12, 17, 23, 4, 29, 11, 24, 31, 5, 21, 27, 13, 18,
    38, 37)
