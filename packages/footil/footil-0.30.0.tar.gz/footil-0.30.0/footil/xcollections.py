"""Module for collections helpers."""
from collections.abc import Sequence


def batch(seq: Sequence, size: int) -> Sequence:
    """Yield sequence in batches by specified size.

    Args:
        seq: sequence to split into batches.
        size: size of a single batch.

    Returns:
        sequence batches

    """
    for i in range(0, len(seq), size):
        yield seq[i:i + size]
