
class switch(object):
    value = None

    def __new__(klass, value):
        klass.value = value
        klass.matched = False
        return True


def case(*args):
    switch.matched = switch.matched or any((arg == switch.value for arg in args))
    return switch.matched
