# Tlabs

## Hiveplots

<img src="plots/agency_actioncats.png" >

1st axis: Egos (Colors by sector - Civil Society: yellow; Academia: blue; Government: green; Private sector: purple).

2nd axis: Alters (same colors by sector).

3rd axis: Practices (in red) ordered by Indegree.

2nd and 3rd axis are linked by practices (light cyan when the indegree is 1 and dark cyan when more).

Actions follow the following order and color scheme:


Practice | Category
--------------------
Research | darkcyan
Training | firebrick
Agricultural/ecological training | orange
Outreach | green
Market | blue
Education | teal
Funding | grey
Collaboration | red
Financial/commercial training | yellow
Social organization | cornflowerblue
Tourism | forestgreen
Management | dodgerblue
Networking | goldenrod
Production | midnightblue
Construction | darkgreen
Culture | cyan
Consultancy | hotpink
Ecological conservation | lightcoral
Citizen assistance | indigo
Legal training | brown


<table>
<thead>
<tr>
<td>
Government
</td>
<td>
Academia
</td>
<td>
Private sector
</td>
<td>
Civil Society
</td>
</tr>
</thead>
<tbody>
<tr>
<td>
<img src="plots/Gobierno_actioncats.png">
</td>
<td>
<img src="plots/Academia_actioncats.png">
</td>
<td>
<img src="plots/Privado_actioncats.png">
</td>
<td>
<img src="plots/Sociedad_Civil_actioncats.png">
</td>
</tr>
</tbody>
</table>


## Clustered Egos by the Alters they share

<img src="plots/dendrogram.png">

Each cell in the heatmap contains the jaccard index of similarity
between both Egos' set of Alters.

## Clustered Egos by the practices they share

<img src="plots/dendrogram_actions.png">

Each cell contains the jaccard index of similarity between both Egos'
set of Practices, which are indirectly joined to an Ego by her Alters.

## Clustered alters by their distances to Egos

<img src="plots/dendrogram_distances.png">

## Alters, Practices clustered by mutual connections

<img src="plots/dendrogram_alters_actions.png">
