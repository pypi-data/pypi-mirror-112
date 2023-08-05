from collections import abc


def is_seq_of(seq, expected_type, seq_type=None):
    """Check whether it is a sequence of some type.

    Args:
        seq (Sequence): The sequence to be checked.
        expected_type (type): Expected type of sequence items.
        seq_type (type, optional): Expected sequence type.

    Returns:
        bool: Whether the obj is the seq of the expected type.
    """
    if not isinstance(expected_type, type):
        raise TypeError(f'Expected type should be type, but got {type(expected_type)}')
    if seq_type is None:
        exp_seq_type = abc.Sequence
    else:
        if not isinstance(seq_type, type):
            raise TypeError(f'Seqence type should be type, but got {type(seq_type)}')
        exp_seq_type = seq_type
    if not isinstance(seq, exp_seq_type):
        return False
    for item in seq:
        if not isinstance(item, expected_type):
            return False
    return True


def is_list_of(seq, expected_type):
    """Check whether it is a list of some type."""
    return is_seq_of(seq, expected_type, seq_type=list)


def is_tuple_of(seq, expected_type):
    """Check whether it is a tuple of some type."""
    return is_seq_of(seq, expected_type, seq_type=tuple)
