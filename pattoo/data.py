"""Data manipulation functions used by pattoo."""


def integerize(value):
    """Convert value to integer.

    Args:
        value: Value to convert

    Returns:
        result: Value converted to iteger

    """
    # Try edge case
    if value is True:
        return None
    if value is False:
        return None

    # Try conversion
    try:
        result = int(value)
    except:
        result = None

    # Return
    return result
