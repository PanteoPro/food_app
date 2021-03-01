def _isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def _isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
