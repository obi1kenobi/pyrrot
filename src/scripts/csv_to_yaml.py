#!/usr/bin/python

import sys
from os import path
# hack to allow this script to run directly
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from src.environment.Environment import Environment
from src.environment.Polygon import Polygon
from src.util.IndentedWriter import IndentedWriter

def print_usage_and_exit():
    print "Usage: python csv_to_yaml.py <csv_obstacles> <csv_features> <yaml_output>"
    sys.exit(1)

def parse_csv_to_polygons(csv):
    lines = csv.readlines()
    return [Polygon.parse_from_csv(x) for x in lines]

def main():
    if len(sys.argv) != 4:
        return print_usage_and_exit()

    csv_obstacles_path = sys.argv[1]
    csv_features_path = sys.argv[2]
    yaml_output_path = sys.argv[3]

    features = []
    obstacles = []

    with open(csv_obstacles_path, "r") as csv:
        obstacles = parse_csv_to_polygons(csv)

    with open(csv_features_path, "r") as csv:
        features = parse_csv_to_polygons(csv)

    with open(yaml_output_path, "w") as yaml:
        writer = IndentedWriter(yaml)
        env = Environment(obstacles, features)
        env.serialize(writer)


if __name__ == '__main__':
    main()
