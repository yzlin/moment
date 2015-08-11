
class switch(object):
    value = None

    def __new__(cls, value):
        cls.value = value
        cls.matched = False
        return True


def case(*args):
    switch.matched = switch.matched or any((arg == switch.value for arg in args))
    return switch.matched
