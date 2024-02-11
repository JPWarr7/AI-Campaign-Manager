INT_MAX = pow(2, 31) - 1


def normalize(value):
    new_value = min(abs(int(value)), INT_MAX)
    print(new_value)
    return new_value
