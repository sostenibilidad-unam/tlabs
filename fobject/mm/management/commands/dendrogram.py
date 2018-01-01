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
        alters = {}

        for ego in Alter.objects.filter(name__contains='TL0'):
            alters[ego] = set([edge.target for edge in ego.ego_net.all()])

        a = []
        for i in sorted(alters.keys()):
            row = []
            for j in sorted(alters.keys()):
                row.append(jaccard_index(alters[i], alters[j]))
            a.append(row)

        df = pd.DataFrame(data=a, columns=sorted(alters.keys()))
        sns.clustermap(df, standard_scale=1,
                       yticklabels=sorted(alters.keys()))
        plt.savefig('dendrogram.png')
