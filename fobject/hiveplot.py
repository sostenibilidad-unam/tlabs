import os, sys
if __name__ == '__main__':
    # Setup environ
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fobject.settings")

    # Setup django
    import django
    django.setup()


from mm.models import Alter, Action, Sector, Agency
from math import sin, cos, radians
from pyveplot import Hiveplot, Node, Axis


h = Hiveplot( 'agency.svg')


def rotate(radius, angle, origin=(0, 0)):
    """ Returns a tuple of destination coordinates
        given a radius, angle and origin tuple """
    return (origin[0] + round((radius * cos(radians(angle))), 2),
            origin[1] + round((radius * sin(radians(angle))), 2))


offcenter = 50
center = (500, 400)
rotation = -180

ego = Sector.objects.get(name='Ego')

ego_count = Alter.objects.filter(sector=ego).count()
ego_axis_origin = rotate(offcenter,
                         angle=rotation,
                         origin=center)
axis_egos = Axis(ego_axis_origin,
                 rotate(offcenter + ego_count * 20,
                        angle=rotation,
                        origin=ego_axis_origin),
                 stroke="purple",
                 stroke_opacity="1", stroke_width=2)



alter_count = Alter.objects.exclude(sector=ego).count()
alter_axis_origin = rotate(offcenter,
                           angle=rotation + 135,
                           origin=center)
axis_alters = Axis(alter_axis_origin,
                   rotate(offcenter + alter_count * 10,
                          angle=rotation + 135,
                          origin=alter_axis_origin),
                   stroke="grey",
                   stroke_opacity="1", stroke_width=2)




action_count = Action.objects.count()
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
for e in Alter.objects.filter(sector=ego).all():
    j += 0.9
    n = Node(e)
    axis_egos.add_node(n, j / ego_count)
    n.dwg = n.dwg.circle(center=(n.x, n.y),
                         r=7,
                         stroke_width=0,
                         fill='darkred',
                         fill_opacity=0.8)



# place alter nodes on alter axis
j = 0.0
for e in Alter.objects.exclude(sector=ego).all():
    j += 1.0
    n = Node(e)
    axis_alters.add_node(n, j / alter_count)
    n.dwg = n.dwg.circle(center=(n.x, n.y),
                         r=3,
                         stroke_width=0,
                         fill='darkgrey',
                         fill_opacity=0.9)





# place action nodes on action axis
j = 0.0
for e in Action.objects.all():
    j += 0.99
    n = Node(e)
    axis_actions.add_node(n, j / action_count)
   
    n.dwg = n.dwg.rect(insert = (n.x - 4, n.y - 4),
                       size   = (8, 8),
                       fill   = 'midnightblue',
                       fill_opacity = 0.5,
                       stroke_width = 0.5)



    
# grab egos
for e in Alter.objects.filter(sector=ego).all():
    # grab their ego net
    for edge in e.ego_net.all():
        a = edge.target
        if a in axis_alters.nodes:
            print e, a        
            h.connect(axis_egos, e,
                      20,
                      axis_alters, a,
                      -45,
                      stroke_width=0.6,
                      stroke_opacity=0.99,
                      stroke='limegreen')
                  


# create links for agencies
for a in Agency.objects.all():
    if a.alter in axis_alters.nodes and a.action in axis_actions.nodes:
        h.connect(axis_alters, a.alter,
                  10,
                  axis_actions, a.action,
                  -10,
                  stroke_width=0.6,
                  stroke_opacity=0.99,
                  stroke='orange')
                  
            
h.save()
