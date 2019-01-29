# coding: utf-8
import sys
import os
import argparse
import networkx as nx

parser = argparse.ArgumentParser(
    description="sum centrality weights for action")

parser.add_argument('--phase', required=True,
                    help='which phase')


args = parser.parse_args()

if __name__ == '__main__':
    # Setup environ
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fobject.settings")

    # Setup django
    import django
    django.setup()

    from mm.models import Alter, Phase

phase = Phase.objects.get(phase=args.phase)


def bag_of_actions(ego):
    for ego_edge in ego.ego_net.filter(phase=phase):
        return [action.action
                for action in ego_edge.target.action_set.filter(phase=phase)]


for ego in Alter.objects.filter(name__startswith='TL0'):
    g = ego.mental_model(phase)
    print ego, nx.centrality.betweenness_centrality(g)
    print ego, bag_of_actions(ego)
