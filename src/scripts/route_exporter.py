#!/usr/bin/python

import sys
from os import path
# hack to allow this script to run directly
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from src.environment.Environment import Environment
from src.environment.Polygon import Polygon
from src.environment.location import Location2D
from src.planning.Planner import Planner
from src.util.IndentedWriter import IndentedWriter

def print_usage_and_exit():
    print "Usage: python route_exporter.py <yaml_environment> <environment_with_route>"
    print ""
    print "Then, type in the route, one feature point per line."
    print "End with an empty line to calculate and export the route."
    sys.exit(1)

def read_validated_feature(valid_names, input_text):
    feature = raw_input(input_text).strip()
    while feature not in valid_names:
        print "*** '%s' is not a valid feature name" % feature
        print "*** Valid names: %s" % str(valid_names)
        feature = raw_input(input_text).strip()
    return feature

def read_route(env):
    route = []
    names = {x.name for x in env.features}
    names.add("")
    feature = read_validated_feature(names, 'Choose the feature at which to start: ')
    while feature != "":
        route.append(feature)
        feature = read_validated_feature(names, '    Choose the next feature to visit: ')
    return route

def create_waypoint_features(waypoints):
    WAYPOINT_BLOCK_LENGTH = 0.4

    features = []
    for i, waypoint in enumerate(waypoints):
        name = "waypoint_%d" % i
        x, y = waypoint
        dlength = WAYPOINT_BLOCK_LENGTH / 2
        corners = [Location2D(x - dlength, y - dlength), \
                   Location2D(x - dlength, y + dlength), \
                   Location2D(x + dlength, y + dlength), \
                   Location2D(x + dlength, y - dlength)]
        features.append(Polygon(name, corners))

    return features

def print_waypoints(waypoints):
    print ""
    print "Found a valid path that visits all features in the given order:"
    for waypoint in waypoints:
        print waypoint
    print ""

def main():
    if len(sys.argv) != 3:
        return print_usage_and_exit()

    input_env_path = sys.argv[1]
    output_env_path = sys.argv[2]

    input_env = None
    output_env = None

    with open(input_env_path, "r") as yaml:
        lines = [l.rstrip() for l in yaml.readlines()]
        input_env, _ = Environment.deserialize(lines, 0)

    planner = Planner(input_env)

    desired_route = read_route(input_env)

    if len(desired_route) < 2:
        raise ValueError("Cannot plan a route with fewer than two features!")

    waypoints = [x for x in planner.route(desired_route)]

    print_waypoints(waypoints)

    # clone the features array
    features = [x for x in input_env.features]
    features.extend(create_waypoint_features(waypoints))

    output_env = Environment(input_env.obstacles, features)

    with open(output_env_path, "w") as yaml:
        writer = IndentedWriter(yaml)
        output_env.serialize(writer)

if __name__ == '__main__':
    main()
