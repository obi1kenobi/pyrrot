from src.util.preconditions import precondition_strings_equal
from src.util.strings import pad_left, count_left_padding
from src.environment.Polygon import Polygon

class Environment(object):
    # obstacles, features are lists of Polygons
    def __init__(self, obstacles, features):
        self.obstacles = obstacles
        self.features = features

    # writer = IndentedWriter
    # this function makes the Environment write itself as YAML into the writer
    def serialize(self, writer):
        writer.write_line("environment:")
        writer.indent()

        writer.write_line("obstacles:")
        writer.indent()
        for obstacle in self.obstacles:
            obstacle.serialize(writer)
        writer.unindent()

        writer.write_line("features:")
        writer.indent()
        for feature in self.features:
            feature.serialize(writer)
        writer.unindent()

        writer.unindent()

    # lines = list of strings
    # this function deserializes a YAML stream into an Environment
    # returns Environment, next_line_index
    # where next_line_index is the index of the first line that was not consumed
    @staticmethod
    def deserialize(lines, next_line_index):
        starting_indentation = count_left_padding(lines[next_line_index])
        assert starting_indentation >= 0

        precondition_strings_equal(lines[next_line_index], pad_left("environment:", starting_indentation))
        precondition_strings_equal(lines[next_line_index + 1], pad_left("obstacles:", starting_indentation + 2))
        next_line_index += 2

        obstacles = []
        features = []

        while next_line_index < len(lines) and \
              lines[next_line_index] != pad_left("features:", starting_indentation + 2):
            polygon, next_line_index = Polygon.deserialize(lines, next_line_index)
            obstacles.append(polygon)

        # advance past line containing "features:"
        next_line_index += 1
        while next_line_index < len(lines) and \
              count_left_padding(lines[next_line_index]) > starting_indentation:
            polygon, next_line_index = Polygon.deserialize(lines, next_line_index)
            features.append(polygon)

        return Environment(obstacles, features), next_line_index
