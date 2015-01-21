from itertools import chain
from collections import defaultdict
from shapely.geometry import polygon, LineString
from src.constants import *
from src.util.iterators import constant_factory
from src.util.preconditions import precondition
import heapq

class Planner(object):
    # environment = src.environment.Environment object
    # route = list of feature names to visit, in that order.
    #         the features must exist in the environment
    def __init__(self, environment):
        self.environment = environment
        self.obstacle_safe_polygons = {}  # dict of obstacle name -> buffered polygon
        self.feature_points = {}          # dict of feature name -> centroid of feature polygon
        self.feature_indexes = {}         # dict of feature name -> index in coords list
        self.coords = []                  # list of (x, y) tuples

        for poly in self.environment.obstacles:
            # create buffered obstacle
            buffered_poly = polygon.orient(poly.shape.buffer( \
                OBSTACLE_SAFE_DISTANCE, \
                resolution=SAFE_DISTANCE_RESOLUTION))

            self.obstacle_safe_polygons[poly.name] = buffered_poly

            # create waypoints
            waypoint_poly = polygon.orient(poly.shape.buffer( \
                WAYPOINT_DISTANCE, \
                resolution=WAYPOINT_RESOLUTION))
            self.coords.extend(waypoint_poly.exterior.coords)

        for poly in self.environment.features:
            # choose the centroids of each feature
            pt = poly.shape.centroid

            # sanity check to ensure the point isn't inside a buffered obstacle
            for obstacle in self.obstacle_safe_polygons.itervalues():
                if obstacle.contains(pt):
                    raise ValueError("Feature centroid was within buffered area of obstacle")

            coords = pt.coords[0]
            self.feature_points[poly.name] = coords
            self.feature_indexes[poly.name] = len(self.coords)
            self.coords.append(coords)

        def dict_generator():
            return defaultdict(constant_factory(float('inf')))

        # initialize connectivity matrix
        self.pairwise_distances = defaultdict(dict_generator)
        for i in xrange(len(self.coords)):
            pta = self.coords[i]
            for j in xrange(i + 1, len(self.coords)):
                ptb = self.coords[j]
                line = LineString([pta, ptb])

                # check the line formed from every pair of coordinates
                # for intersections against every buffered obstacle polygon
                valid = True
                for poly in self.obstacle_safe_polygons.itervalues():
                    if line.intersects(poly):
                        valid = False
                        break

                if valid:
                    self.pairwise_distances[pta][ptb] = line.length
                    self.pairwise_distances[ptb][pta] = line.length


    # Calculate a route that starts at the first location in the path list
    # and visits every subsequent location, ending at the last location.
    #
    # path = list of feature names (strings)
    # returns list of (x, y) tuples representing locations to fly to
    def route(self, path):
        precondition(len(path) >= 2, "The path cannot have fewer than two locations")

        from_locations = path[:-2]
        to_locations = path[1:]
        path_legs = zip(from_locations, to_locations)
        return chain.from_iterable([self.directions(leg[0], leg[1]) for leg in path_legs])

    # Calculate a set of directions to get from the given starting point to the end point
    # from_feature, to_feature = feature names (strings)
    # returns a list of (x, y) tuples representing locations to fly to (not including the start)
    def directions(self, from_feature, to_feature):
        precondition(from_feature in self.feature_indexes, "Unknown feature name %s" % from_feature)
        precondition(to_feature in self.feature_indexes, "Unknown feature name %s" % to_feature)

        NOT_VISITED = -1
        ROOT = -2
        INFINITY = float('inf')

        point_distances = defaultdict(constant_factory(INFINITY))
        point_ancestors = defaultdict(constant_factory(NOT_VISITED))

        from_index = self.feature_indexes[from_feature]
        to_index = self.feature_indexes[to_feature]

        # run Dijkstra's algorithm / Uniform Cost Search
        heap = [(0.0, from_index, ROOT)]
        while len(heap) > 0 and point_ancestors[to_index] == NOT_VISITED:
            distance, current_index, origin_index = heapq.heappop(heap)
            if point_ancestors[current_index] != NOT_VISITED:
                continue

            current_pt = self.coords[current_index]
            point_ancestors[current_index] = origin_index
            point_distances[current_index] = distance
            for next_index in xrange(len(self.coords)):
                next_pt = self.coords[next_index]
                total_distance = distance + self.pairwise_distances[current_pt][next_pt]
                if total_distance < point_distances[next_index]:
                    heapq.heappush(heap, (total_distance, next_index, current_index))

        if point_ancestors[to_index] == -1:
            raise ValueError("Could not find path from '%s' to '%s'" % (from_feature, to_feature))

        # follow path backward from destination to source
        path = [self.coords[to_index]]
        current_index = point_ancestors[to_index]
        while current_index != from_index:
            path.append(self.coords[current_index])
            current_index = point_ancestors[current_index]

        return reversed(path)
