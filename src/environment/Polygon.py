from location import Location2D

class Polygon(object):
    # name is a string not containing ":" or whitespace chars
    # corners is a list of tuples of (x, y) coordinates
    def __init__(self, name, corners):
        assert ":" not in name
        assert " " not in name
        assert "\n" not in name
        self.name = name
        self.corners = corners

    # writer is an IndentedWriter
    # this function makes the Polygon write itself as YAML into the writer
    def serialize(self, writer):
        writer.write_line(self.name + ":")

        writer.indent()
        writer.write_line("shape: polygon")
        writer.write_line("corners:")

        writer.indent()
        for corner in self.corners:
            writer.write_line("- [%.3f, %.3f]" % (corner.x, corner.y))
        writer.unindent()

        writer.unindent()

    @staticmethod
    def parse_from_csv(csv_line):
        args = csv_line.strip().split(',')
        assert len(args) >= 4
        name = args[0].strip().replace(' ', '_').\
                               replace('(', '').\
                               replace(')', '')
        corners = [Location2D.parse(x) for x in args[1:]]
        return Polygon(name, corners)
