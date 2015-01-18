class Location2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # format example: [-1.0; 2.0]
    @staticmethod
    def parse(loc_string):
        args = loc_string.strip().strip('[]').split(';')
        x = float(args[0])
        y = float(args[1])
        return Location2D(x, y)


class Location3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # format example: [-1.0; 2.0; 3.5]
    @staticmethod
    def parse(loc_string):
        args = loc_string.strip().strip('[]').split(';')
        x = float(args[0])
        y = float(args[1])
        z = float(args[2])
        return Location3D(x, y, z)

