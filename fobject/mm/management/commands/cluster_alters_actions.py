from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
from mm.models import Alter, ActionEdge, Action

import seaborn as sns
import pandas as pd


class Command(BaseCommand):
    help = 'draw dendrogram'

    def handle(self, *args, **options):
        t = []
        for alter in Alter.objects.exclude(
                name__startswith='TL0').order_by('id'):
            r = []
            for action in Action.objects.order_by('id'):
                agency = ActionEdge.objects.filter(alter=alter,
                                               action=action).count()
                r.append(agency)
            t.append(r)

        df = pd.DataFrame(data=t,
                          columns=[a.action
                                   for a in
                                   Action.objects.order_by('id')])

        cm = sns.clustermap(df, cmap="Blues",
                            yticklabels=[a.name for a in
                                         Alter.objects.exclude(
                                             name__startswith='TL0'
                                         ).order_by('id')],
                            figsize=(40, 40))

        plt.setp(cm.ax_heatmap.yaxis.get_majorticklabels(), fontsize=7)
        plt.setp(cm.ax_heatmap.xaxis.get_majorticklabels(), fontsize=7)
        cm.cax.set_visible(False)

        plt.savefig('dendrogram_alters_actions.svg')
