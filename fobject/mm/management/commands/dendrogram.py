from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
from mm.models import Alter, Agency, Action
from pprint import pprint

from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage

import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt


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

        #plt.imshow(a, cmap='hot', interpolation='nearest')
        #plt.show()

        #dist_mat = a
        #linkage_matrix = linkage(dist_mat,
        #                         "single")

        # dendrogram(linkage_matrix,
        #            color_threshold=1,
        #            labels=alters.keys(),
        #            show_leaf_counts=True)
        # plt.show()

        df = pd.DataFrame(data=a, columns=sorted(alters.keys()))
        sns.clustermap(df, standard_scale=1)
        plt.savefig('dendrogram.png')
