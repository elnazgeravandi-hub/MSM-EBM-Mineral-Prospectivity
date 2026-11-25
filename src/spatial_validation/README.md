# Buffered spatial cross-validation

`buffered_cv.py` implements the fixed-coordinate-origin spatial block assignment, five-fold allocation, and candidate training-cell exclusion for distances <= the buffer. The optional shared-occurrence exclusion is a sensitivity test, not independent validation. All model comparisons reuse partitions.
