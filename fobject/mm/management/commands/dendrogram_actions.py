from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
from mm.models import Alter

import seaborn as sns
import pandas as pd


def jaccard_index(first, *others):
    """ Computes jaccard index """
    return float(len(first.intersection(*others))) \
        / float(len(first.union(*others)))


class Command(BaseCommand):
    help = 'draw dendrogram'

    def handle(self, *args, **options):
        actions = {}

        for ego in Alter.objects.filter(name__contains='TL0'):
            actions[ego] = set()
            for edge in ego.ego_net.all():
                for action in edge.target.action_set.all():
                    actions[ego].add(action)

        a = []
        for i in sorted(actions.keys()):
            row = []
            for j in sorted(actions.keys()):
                row.append(jaccard_index(actions[i], actions[j]))
            a.append(row)

        df = pd.DataFrame(data=a, columns=sorted(actions.keys()))
        cg = sns.clustermap(df, standard_scale=1,
                            yticklabels=sorted(actions.keys()))

        plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=45)
        plt.savefig('dendrogram_actions.png')
