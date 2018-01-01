from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
from mm.models import Alter, EgoEdge

import seaborn as sns
import pandas as pd


class Command(BaseCommand):
    help = 'draw dendrogram'

    def handle(self, *args, **options):
        t = []
        for alter in Alter.objects.exclude(
                name__contains='TL0').order_by('id'):
            r = []
            for ego in Alter.objects.filter(
                    name__contains='TL0').order_by('id'):
                try:
                    edge = EgoEdge.objects.get(source=ego, target=alter)
                    distance = 4 - edge.distance
                except EgoEdge.DoesNotExist:
                    distance = 0
                r.append(distance)
            t.append(r)

        df = pd.DataFrame(data=t,
                          columns=[a.name
                                   for a in
                                   Alter.objects.filter(
                                       name__contains='TL0').order_by('id')])

        cm = sns.clustermap(df, cmap="Blues",
                            yticklabels=[e.name for e in
                                         Alter.objects.exclude(
                                             name__contains='TL0'
                                         ).order_by('id')],
                            figsize=(8, 24))

        hm = cm.ax_heatmap.get_position()
        plt.setp(cm.ax_heatmap.yaxis.get_majorticklabels(), fontsize=7)
        plt.setp(cm.ax_heatmap.xaxis.get_majorticklabels(), fontsize=9)
        cm.ax_heatmap.set_position([hm.x0, hm.y0,
                                    hm.width * 0.4, hm.height])
        col = cm.ax_col_dendrogram.get_position()
        cm.ax_col_dendrogram.set_position([col.x0,
                                           col.y0,
                                           col.width * 0.4,
                                           col.height * 0.4])

        plt.setp(cm.ax_heatmap.xaxis.get_majorticklabels(), rotation=70)
        plt.savefig('dendrogram_distances.png')
