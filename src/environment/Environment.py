class Environment(object):
    # obstacles, features are lists of Polygons
    def __init__(self, obstacles, features):
        self.obstacles = obstacles
        self.features = features

    # writer is an IndentedWriter
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
