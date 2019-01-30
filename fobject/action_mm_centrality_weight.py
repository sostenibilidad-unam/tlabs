# coding: utf-8
import sys
import os
import argparse
import networkx as nx
import pandas as pd
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline



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

    from mm.models import Alter, Phase, ActionEdge, Variable

phase = Phase.objects.get(phase=args.phase)

actions_centrality_sum = {action.action: {var.name: 0.0
                                          for var in Variable.objects.all()}
                          for action in ActionEdge.objects.filter(phase=phase)}


def bag_of_actions(ego):
    for ego_edge in ego.ego_net.filter(phase=phase):
        return [action.action
                for action in ego_edge.target.action_set.filter(phase=phase)]


def upsert(dsum, acc, con, v):

    if acc in dsum:
        if con in dsum[acc]:
            dsum[acc][con] += v
        else:
            dsum[acc][con] = v
    else:
        dsum[acc] = {con: v}


all_actions = set([])
all_vars = set([])

# sum mental model variable centralities from Egos for all actions
for ego in Alter.objects.filter(name__startswith='TL0'):
    g = ego.mental_model(phase)
    centralities = nx.centrality.betweenness_centrality(g)

    for action in bag_of_actions(ego):
        all_actions.add(action)
        for variable in centralities:
            all_vars.add(variable)
            upsert(actions_centrality_sum,
                   action,
                   variable, centralities[variable])


rows = {}

for action in actions_centrality_sum:
    if sum(actions_centrality_sum[action].values()) > 0:
        rows[action] = actions_centrality_sum[action].values()


df = pd.DataFrame.from_dict(rows,
                            orient='index',
                            columns=[unicode(v.name) for v in Variable.objects.all()])

df.drop([v for v in df.columns if df[v].sum() == 0], axis=1)
#sns.heatmap(df, annot=True)
plt.pcolor(df)
#plt.ylabels(df.index)
plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
#plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
plt.show()
