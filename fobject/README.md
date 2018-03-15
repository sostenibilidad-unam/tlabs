# F-Object

The [T-Labs platform](http://tlabs.magrat.mine.nu) is a web
application that handles:

 - administration of network data (creation, update, delete).
 - exploration and visualization of networks


## Relational Database

The structure of a network is precisely in the relationships among its
nodes. A relational database adequately captures the relationships
between Egos, Alters, Practices, etc.

![table design](db_tables.png)

The T-Labs platform is built on the [Django](http://djangoproject.com)
framework.  One of Django's features is an Object Relational Mapper
which makes it easy to model such a database.

An convenient
[administration interface](http://tlabs.magrat.mine.nu/admin) is then
built on top of this model.

## Network visualizaton and analysis

Having the data loaded into a database makes it readily available to
[NetworkX](https://networkx.github.io), a Python library for studying
graphs and netwoks. We use it to measure structural traits of our
networks, such as connectivity degree of nodes or average shortest
path length between nodes.

Interactive exploration and visualization of the data is possible
through the web interface, which uses the
[Cytoscape.js](http://js.cytoscape.org) library.
