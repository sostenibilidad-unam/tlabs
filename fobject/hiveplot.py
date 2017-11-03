import os, sys
if __name__ == '__main__':
    # Setup environ
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fobject.settings")

    # Setup django
    import django
    django.setup()


from mm.models import Alter, Action, Sector, Agency, Networks

#n = Networks()
#n.update_alter_metrics()
#n.update_action_metrics()

from math import sin, cos, radians
from scale import Scale
from pyveplot import Hiveplot, Node, Axis


h = Hiveplot( 'agency.svg')


def rotate(radius, angle, origin=(0, 0)):
    """ Returns a tuple of destination coordinates
        given a radius, angle and origin tuple """
    return (origin[0] + round((radius * cos(radians(angle))), 2),
            origin[1] + round((radius * sin(radians(angle))), 2))


offcenter = 80
center = (500, 400)
rotation = -180

ego = Sector.objects.get(name='Ego')

ego_count = Alter.objects.filter(sector=ego).count()
ego_scale = Scale(domain=[Alter.objects.order_by('degree')[0].degree,
                          Alter.objects.order_by('-degree')[0].degree],
                  range=[5, 30])
ego_axis_len = sum([ego_scale.linear(e.degree)*2.0 for e in Alter.objects.filter(sector=ego).all()])

ego_axis_origin = rotate(offcenter,
                         angle=rotation,
                         origin=center)
axis_egos = Axis(ego_axis_origin,
                 rotate(offcenter + ego_axis_len,
                        angle=rotation,
                        origin=ego_axis_origin),
                 stroke="purple",
                 stroke_opacity="1", stroke_width=2)



alter_count = Alter.objects.exclude(sector=ego).count()
alter_scale = Scale(domain=[Alter.objects.exclude(sector=ego).order_by('degree')[0].degree,
                            Alter.objects.exclude(sector=ego).order_by('-degree')[0].degree],
                  range=[5, 30])
alter_axis_len = sum([alter_scale.linear(e.degree) for e in Alter.objects.exclude(sector=ego).all()])

alter_axis_origin = rotate(offcenter,
                           angle=rotation + 135,
                           origin=center)
axis_alters = Axis(alter_axis_origin,
                   rotate(offcenter + alter_axis_len,
                          angle=rotation + 135,
                          origin=alter_axis_origin),
                   stroke="grey",
                   stroke_opacity="1", stroke_width=2)




action_count = Action.objects.count()
action_scale = Scale(domain=[Action.objects.order_by('in_degree')[0].in_degree,
                             Action.objects.order_by('-in_degree')[0].in_degree],
                     range=[5, 30])
action_axis_len = sum([action_scale.linear(a.in_degree)*1.1 for a in Action.objects.all()])

action_axis_origin = rotate(offcenter,
                            angle=rotation + 180 + 45,
                            origin=center)
axis_actions = Axis(action_axis_origin,
                    rotate(offcenter + action_count * 10,
                           angle=rotation + 180 + 45,
                           origin=action_axis_origin),
                    stroke="blue",
                    stroke_opacity="1", stroke_width=2)

h.axes = [axis_egos, axis_alters, axis_actions]

# place ego nodes on ego axis
j = 0.0
for e in Alter.objects.filter(sector=ego).order_by('degree').all():
    delta = ego_scale.linear(e.degree) / ego_axis_len
    j += delta * 2.0        
    n = Node(e)
    axis_egos.add_node(n, j)
    n.dwg = n.dwg.circle(center=(n.x, n.y),
                         r=ego_scale.linear(e.degree),
                         stroke_width=0,
                         fill='darkred',
                         fill_opacity=0.8)


sector_color = {'Academia': 'forestgreen',
               'Gobierno': 'greenyellow',
               None: 'blue',
               'Otros': 'gold',
               'Privado': 'orangered',
               ' Sociedad_Civil': 'deeppink',
               'Sociedad_Civil': 'deeppink'}

# place alter nodes on alter axis
j = 0.0
for e in Alter.objects.exclude(sector=ego).order_by('degree').all():
    delta = alter_scale.linear(e.degree) / alter_axis_len
    j += delta
    print e.degree, delta, j, alter_scale.linear(e.degree)  # / ego_axis_len  #, ego_offset.linear()

    n = Node(e)
    axis_alters.add_node(n, j)
    if e.sector:
        sector = e.sector.name
    else:
        sector = None
    n.dwg = n.dwg.circle(center=(n.x, n.y),
                         r=alter_scale.linear(e.degree)/2.0,
                         stroke_width=0,
                         fill=sector_color[sector],
                         fill_opacity=0.77)


# place action nodes on action axis
j = 0.0
for action in Action.objects.order_by('in_degree'):
    delta = 1.1 * action_scale.linear(action.in_degree) / action_axis_len
    j += delta
    print action.in_degree, delta, j, action_scale.linear(action.in_degree)  # / ego_axis_len  #, ego_offset.linear()
    
    n = Node(action)
    axis_actions.add_node(n, j)
    size = action_scale.linear(action.in_degree)
    n.dwg = n.dwg.rect(insert = (n.x - size/2.0,
                                 n.y - size/2.0),
                       size   = (size, size),
                       fill   = 'midnightblue',
                       fill_opacity = 0.6,
                       stroke_width = 0.5)



ego_color = {1: 'forestgreen',
             2: 'greenyellow',
             3: 'goldenrod',
             4: 'gold'}
             
             
    
# grab egos
for e in Alter.objects.filter(sector=ego).all():
    # grab their ego net
    for edge in e.ego_net.all():
        a = edge.target
        if a in axis_alters.nodes:
            h.connect(axis_egos, e,
                      20,
                      axis_alters, a,
                      -45,
                      stroke_width=1,
                      stroke_opacity=1,
                      stroke=ego_color[edge.distance],)
                  


# create links for agencies
for a in Agency.objects.all():
    if a.alter in axis_alters.nodes and a.action in axis_actions.nodes:
        if a.action.in_degree < 2:
            color = "pink"
        else:
            color = "royalblue"
        h.connect(axis_alters, a.alter,
                  10,
                  axis_actions, a.action,
                  -10,
                  stroke_width=0.99,
                  stroke_opacity=0.7,
                  stroke=color)
                  
            
h.save()
