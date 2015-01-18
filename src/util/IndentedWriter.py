class IndentedWriter(object):
    # stream can be an opened file stream or any other class
    # that has a "write" method which takes a string
    def __init__(self, stream):
        self.stream = stream
        self.indents = 0

    def indent(self):
        self.indents += 2

    def unindent(self):
        self.indents -= 2
        assert self.indents >= 0

    def write_line(self, s):
        if self.indents > 0:
            self.stream.write(" " * self.indents)
        self.stream.write(s)
        self.stream.write('\n')

