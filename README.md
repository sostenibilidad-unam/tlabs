# tlabs

Transofrmation Labs

## Hiveplot

### Ejes y nodos
 1. Los círculos rojos son Egos, van ordenados por grado de conectividad.
 2. Sobre el eje gris, en orden de conectividad, Alters. Sus colores representan su sector:
   - Academia: forestgreen
   - Gobierno: greenyellow
   - Otros: gold
   - Privado: orangered
   - Sociedad_Civil: deeppink
   - Sociedad_Civil: deeppink
   - None: blue <--- *algunos alters no tienen sector*
 3. Cuadros azules son acciones, van ordenadas hacia afuera por in_degree.


## Vínculos

Unen a los ejes 1 y 2 vínculos cuyos colores representan la distancia:

 - distancia 1: forestgreen
 - distancia 2: greenyellow
 - distancia 3: goldenrod
 - distancia 4: gold


Los ejes 2 y tres se unen por vínculos color rosa cuando el in_degree
de la acción es 1, y azul cuando es mayor.

<img src="fobject/agency.png" >
