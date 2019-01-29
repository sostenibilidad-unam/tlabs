# coding: utf-8

import os
import sys
import argparse
import svgwrite
from math import sin, cos, radians
from scale import Scale
from pyveplot import Hiveplot, Node, Axis


parser = argparse.ArgumentParser(
    description="create tlabs hiveplot")

parser.add_argument('--sector',
                    default='all',
                    help='plot which sector')

parser.add_argument('--phase', required=True,
                    help='plot which phase')

parser.add_argument('--egos', nargs="+",
                    help='just plot these egos')


args = parser.parse_args()

if __name__ == '__main__':
    # Setup environ
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fobject.settings")

    # Setup django
    import django
    django.setup()

    from mm.models import Alter, Category, ActionEdge, Networks, Phase

phase = Phase.objects.get(phase=args.phase)

if args.egos is not None:
    egos = [Alter.objects.get(name=ego_name)
            for ego_name in args.egos]
else:
    egos = None

n = Networks()
n.update_alter_metrics()
n.update_action_metrics()


if egos is None:
    name = "ana_hiveplot_%s.svg" % args.phase
else:
    name = "ana_hiveplot_%s_%s.svg" % (args.phase,
                                       "-".join(args.egos))

h = Hiveplot(name)


def rotate(radius, angle, origin=(0, 0)):
    """ Returns a tuple of destination coordinates
        given a radius, angle and origin tuple """
    return (origin[0] + round((radius * cos(radians(angle))), 2),
            origin[1] + round((radius * sin(radians(angle))), 2))


sector_color = {
    'Ego': '#e41a1c',
    'Academia': '#377eb8',
    'Gobierno': '#4daf4a',
    None: '#984ea3',
    'Otros': '#ff7f00',
    'Privado': '#ffff33',
    'Sociedad_Civil': '#cab2d6'

}


offcenter = 80
center = (500, 400)
rotation = -180

############
# Ego axis #
############
ego_count = Alter.objects.filter(name__contains='TL0').count()
ego_scale = Scale(domain=[Alter.objects.order_by('degree')[0].degree,
                          Alter.objects.order_by('-degree')[0].degree],
                  range=[5, 30])
ego_axis_len = sum([ego_scale.linear(e.degree) * 2.0
                    for e in Alter.objects.filter(name__contains='TL0').all()])

ego_axis_origin = rotate(offcenter + 100,
                         angle=rotation,
                         origin=center)
axis_egos = Axis(ego_axis_origin,
                 rotate(offcenter + ego_axis_len,
                        angle=rotation,
                        origin=ego_axis_origin),
                 stroke="purple",
                 stroke_opacity="1", stroke_width=2)

# place ego nodes on ego axis
j = 0.0
for e in Alter.objects.filter(name__contains='TL0').order_by('degree').all():
    delta = ego_scale.linear(e.degree) / ego_axis_len
    j += delta * 2.0
    n = Node(e)
    axis_egos.add_node(n, j)

    if e.sector:
        sector = e.sector.name
    else:
        sector = None

    n.dwg.add(n.dwg.circle(center=(n.x, n.y),
                           r=ego_scale.linear(e.degree),
                           stroke_width=0,
                           fill=sector_color[sector],
                           fill_opacity=0.8))
    g = svgwrite.container.Group(transform='rotate(-90, %s, %s)' % (n.x, n.y),
                                 style='font-size:22')
    g.add(n.dwg.text(e.name,
                     insert=(n.x - 100, n.y)))
    n.dwg.add(g)



alter_scale = Scale(
    domain=[Alter.objects.exclude(name__contains='TL0').
            order_by('degree')[0].degree,
            Alter.objects.exclude(name__contains='TL0').
            order_by('-degree')[0].degree],
    range=[5, 20])


def alter_axis_len(sector_name):
    return sum([alter_scale.linear(a.degree)
                for a in Alter.objects.filter(
                        sector__name=sector_name).exclude(
                            name__contains='TL0')])


##############
# Alter axes #
##############
starts = []


def alter_axis(name, start):

    axis_len = alter_axis_len(name)
    axis_end = rotate(axis_len,
                      angle=rotation + 135,
                      origin=start)
    fake_end = rotate(axis_len + 60,
                      angle=rotation + 135,
                      origin=start)

    starts.append(fake_end)
    axis = Axis(start,
                axis_end,
                stroke=sector_color[name],
                stroke_opacity="1", stroke_width=2)

    # place alter nodes on alter axis
    j = 0.0
    for alter in Alter.objects.filter(
            sector__name=name).exclude(
                name__contains='TL0').order_by('degree').all():
        delta = alter_scale.linear(alter.degree) / axis_len
        j += delta
        n = Node(alter)
        axis.add_node(n, j)

        n.dwg = n.dwg.circle(center=(n.x, n.y),
                             r=alter_scale.linear(alter.degree) / 2.0,
                             stroke_width=0,
                             fill=sector_color[name],
                             fill_opacity=0.87)

    return axis


actioncat_count = Category.objects.count()
actioncat_scale = Scale(
    domain=[min([c.get_degree() for c in Category.objects.all()]),
            max([c.get_degree() for c in Category.objects.all()])],
    range=[20, 100])

action_axis_len = sum([actioncat_scale.linear(c.get_degree())*1.55
                       for c in Category.objects.all()])

action_axis_origin = rotate(offcenter + 80,
                            angle=rotation + 180 + 45,
                            origin=center)

axis_actions = Axis(action_axis_origin,
                    rotate(offcenter + action_axis_len,
                           angle=rotation + 180 + 45,
                           origin=action_axis_origin),
                    stroke="black",
                    stroke_opacity="0.33", stroke_width=1)

# '#cab2d6','#6a3d9a','#ffff99','#b15928']

action_cat_color = {
    'Research': '#8dd3c7',
    'Training': '#ffffb3',
    'Agricultural/ecological training': '#bebada',
    'Outreach': '#fb8072',
    'Market': '#80b1d3',
    'Education': '#fdb462',
    'Funding': '#b3de69',
    'Collaboration': '#fccde5',
    'Financial/commercial training': '#d9d9d9',
    'Social organization': '#bc80bd',
    'Tourism': '#ccebc5',
    'Management': '#ffed6f',
    'Networking': '#a6cee3',
    'Production': '#1f78b4',
    'Construction': '#b2df8a',
    'Culture': '#33a02c',
    'Consultancy': '#fb9a99',
    'Ecological conservation': '#e31a1c',
    'Citizen assistance': '#fdbf6f',
    'Legal training': '#ff7f00'
}


# place action category nodes on action axis

urban = [
    'Funding',
    'Management',
    'Management',
    'Outreach',
    'Construction',
    'Construction',
    'Citizen assistance',
    'Legal training',
    'Management', ]

agro = [
    'Collaboration',
    'Research',
    'Agricultural/ecological training',
    'Agricultural/ecological training',
    'Financial/commercial training',
    'Tourism',
    'Ecological conservation',
    'Agricultural/ecological training',
    'Production',
    'Education',
    'Market',
    'Financial/commercial training',
    'Agricultural/ecological training',
    'Education',
    'Collaboration',
    'Collaboration',
    'Training',
    'Education'
    ]


def by_degree(cat):
    return cat.get_degree()


j = 0.0

for cat in sorted(Category.objects.all(), key=by_degree):
    delta = 0.8 * actioncat_scale.linear(cat.get_degree()) / action_axis_len
    j += delta

    n = Node(cat)
    axis_actions.add_node(n, j)
    j += delta

    size = actioncat_scale.linear(cat.get_degree())
    fill = action_cat_color[cat.name]
    if cat.name in urban:
        n.dwg.add(n.dwg.rect(insert=(n.x - size/2.0,
                                     n.y - size/2.0),
                             size=(size, size),
                             fill=fill,
                             fill_opacity=0.8,
                             stroke_width=0.5))
    elif cat.name in agro:
        n.dwg.add(n.dwg.circle(center=(n.x, n.y),
                               r=size * 0.77,
                               stroke_width=0,
                               fill=fill,
                               fill_opacity=0.8))
    else:
        n.dwg.add(n.dwg.circle(center=(n.x, n.y),
                               r=size * 0.77,
                               stroke_width=0,
                               fill=fill,
                               fill_opacity=0.5))
        n.dwg.add(n.dwg.rect(insert=(n.x - size/2.0,
                                     n.y - size/2.0),
                             size=(size, size),
                             fill=fill,
                             fill_opacity=0.7,
                             stroke_width=0.5))


    g = svgwrite.container.Group(style='font-size:23;')
    g.add(n.dwg.text(cat.name,
                     insert=(n.x - size * 0.83, n.y + 7),
                     text_anchor='end'))
    n.dwg.add(g)


ego_color = {1: 'forestgreen',
             2: 'greenyellow',
             3: 'goldenrod',
             4: 'gold'}


axis_origin = rotate(offcenter,
                     angle=rotation + 135,
                     origin=center)
alter_axes = [alter_axis("Gobierno", axis_origin),
              alter_axis("Academia", starts.pop()),
              alter_axis("Otros", starts.pop()),
              alter_axis("Privado", starts.pop()),
              alter_axis("Sociedad_Civil", starts.pop())]

h.axes = [axis_egos, ] + alter_axes + [axis_actions, ]


# link egos
for ego in Alter.objects.filter(name__contains='TL0').all():
    # grab their ego net
    for edge in ego.ego_net.filter(phase=phase):
        alter = edge.target
        for alter_axis in alter_axes:
            if egos is None or ego in egos:
                if alter in alter_axis.nodes \
                   and (args.sector == 'all'
                        or alter.sector.name == args.sector):
                    h.connect(axis_egos, ego,
                              45,
                              alter_axis, alter,
                              -15,
                              stroke_width=edge.distance * 2.0,
                              stroke_opacity=0.33,
                              stroke=sector_color[alter.sector.name],)


# create set of actions reached by args.egos
action_edges = []
for ae in ActionEdge.objects.filter(phase=phase):
    for ee in ae.alter.ego_net.filter(phase=phase):
        if egos is not None and (ee.source in egos or ee.target in egos):
            action_edges.append(ae)

# create links for agencies
for a in ActionEdge.objects.filter(phase=phase):
    for alter_axis in alter_axes:
        if a in action_edges or action_edges == []:
            if a.alter in alter_axis.nodes \
               and a.action.category in axis_actions.nodes\
               and (args.sector == "all"
                    or a.alter.sector.name == args.sector):
                color = action_cat_color[a.action.category.name]
                opacity = 0.5
                h.connect(alter_axis, a.alter,
                          33,
                          axis_actions, a.action.category,
                          -40,
                          stroke_width=1.5,
                          stroke_opacity=opacity,
                          stroke=color)


h.save()
