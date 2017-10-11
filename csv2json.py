import networkx as nx
import csv
import argparse
from pprint import pprint
import json

parser = argparse.ArgumentParser(
    description='convert edgelist in csv to d3 compatible json')

parser.add_argument('csv', type=argparse.FileType('r'),
                    help='csv input')
parser.add_argument('json', type=argparse.FileType('w'),
                    help='json output')


args = parser.parse_args()


r = csv.DictReader(args.csv)

g = nx.Graph()

for row in r:
    g.add_edge(row['SOURCE'],
               row['TARGET'],
               distance=row['DISTANCE'],
               interaction=row['INTERACTION'])

args.json.write(json.dumps(nx.node_link_data(g), indent=2))
