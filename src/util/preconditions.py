# this method ensures that value is True
# or throws a ValueError with the specified message
def precondition(value, msg):
    if not value:
        raise ValueError(msg)

def precondition_strings_equal(stra, strb):
    if stra != strb:
        raise ValueError("Expected '%s' to equal '%s'" % (stra, strb))
