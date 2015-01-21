from location import Location2D
from src.util.preconditions import precondition, precondition_strings_equal
from src.util.strings import pad_left, count_left_padding
from itertools import permutations
import shapely.geometry as geometry

class Polygon(object):
    # name is a string not containing ":" or whitespace chars
    # corners is a list of Location2D objects
    def __init__(self, name, corners):
        assert ":" not in name
        assert " " not in name
        assert "\n" not in name
        self.name = name
        points = [(p.x, p.y) for p in corners]
        for perm in permutations(points):
            self.shape = geometry.Polygon(perm)
            if self.shape.is_valid:
                self.shape = geometry.polygon.orient(self.shape)
                break

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
    def _mangle_name(name):
        return name.strip().strip(':').replace(' ', '_').\
                                       replace('(', '').\
                                       replace(')', '')

    @staticmethod
    def parse_from_csv(csv_line):
        args = csv_line.strip().split(',')
        assert len(args) >= 4
        name = Polygon._mangle_name(args[0])
        corners = [Location2D.parse(x) for x in args[1:]]
        return Polygon(name, corners)

    @staticmethod
    def deserialize(lines, next_line_index):
        starting_indentation = count_left_padding(lines[next_line_index])
        name = Polygon._mangle_name(lines[next_line_index])
        next_line_index += 1

        precondition_strings_equal(lines[next_line_index], pad_left("shape: polygon", starting_indentation + 2))
        next_line_index += 1

        precondition_strings_equal(lines[next_line_index], pad_left("corners:", starting_indentation + 2))
        next_line_index += 1

        corners = []

        while next_line_index < len(lines) and \
              count_left_padding(lines[next_line_index]) > starting_indentation:
            line = lines[next_line_index].strip()
            precondition(line.startswith("- ["), "Expected line %s to start with '- ['" % line)
            precondition(line.endswith("]"), "Expected line %s to end with ']'" % line)

            arg = line.strip('-').strip().replace(',', ';')
            corners.append(Location2D.parse(arg))
            next_line_index += 1

        return Polygon(name, corners), next_line_index
