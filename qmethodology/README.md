# Q-Methodology analysis for T-Lab

## Methodological annex

Q-Methodology is used to analyze subjective perspectives of a diverse group of participants regarding a particular issue (Webler et al. 2009; Zabala 2014). For this study, Q-Methodology was used as a complementary method to understand the conceptualization of the problem space and the system of values from the T-Lab participants that were later translated into narratives. This methodology is based on analyzing the consensus and disagreements among a group of diverse actors with respect to a series of statements related to a particular issue. These statements are sorted by each participant by ranking them in a range from the statements that a participant most agree with (max. value +4) to the ones that a participant most disagree with (max. value -4), leaving in the middle the statements with a neutral opinion. The statements are placed in a pyramid shape as shown in the figure below.

<img src="qpyramid.png">

For this study, we used 28 statements based on 4 themes related to the case study of the Xochimilco urban wetland: property rights, identity and values, pressures in the ecosystem, and livelihoods. The statements are listed below:

Land use and property rights:
1.- All Mexican homes should have the right to use their land for the benefit of their children.
2.- The land use of chinampas should be exclusively for agriculture.
9.- The main cause for the chinampas urbanization is the lack of public policies implementation.
17.- It is possible to convert the land use of chinampas to urban without degrading the Xochimilco lake.

Patrimony, identity, value:
3.- The chinampas are the patrimony of Xochimilco families.
4.- The chinampa represents the patrimony of all Mexicans.
6.- The chinampa is an important element of the Xochimilco identity.
10.- Xochimilco festivities should be preserved as they are part of Mexico’s history.
11.- Xochimilco ancentral stories are still told (e.g. “La Llorona”).
12.- Xochimilco as a priority site for biodiversity conservation is overrated.
20.- People who live in Xochimilco value the importance of the lake area as an ecological and cultural patrimony.
21.- The festivities are important for the chinampas activities.
22.- The chinampa producers are still devoted to their Saints.
23.- It is important to bless the chinampas and their agricultural products.
25.- People who are not native to Xochimilco are problematic because they do not know anything about it or do not care.
26.- People in general have no idea of the benefits of Xochimilco and how to preserve it.

Ecological conditions and stressors:
7.- Urbanization is destroying Xochimilco.
13.- Biodiversity conservation is important to preserve Xochimilco.
14.- The trajineras boats for tourism is the main cause of the Xochimilco lake degradation.
15.- The trajineras boats are important to preserve Xochimilco.
18.- The agricultural use of the chinampas is affecting the ecology of the Xochimilco lake.
19.- The lake area of Xochimilco is in a good ecological condition.
27.- It is a municipality obligation to maintain the Xochimilco canals in a good condition (cleaning and uncloging them).
28.- All inhabitants and visitors of Xochimilco must keep the area clean.

Livelihoods:
5.- The chinampas are important for the subsistence of Xochimilco families.
8.- People build their houses on the chinampas because they do not have other alternatives for living.
16.- Lots of young people aspire to continue the traditional agricultural practices in the chinampas.
24.- The sons of chinampa producers are looking for different jobs.

The Q-Methodology was applied to the 13 participants in two moments, T0 for the baseline narratives, and T1 for the potential change in narratives. All participants Q-sorts, were statistically analyzed with the software RStudio version 1.0.136 (R Core Team 2016) using the qmethod package for R (Zabala 2014). Statistical Q-analysis is based in a factor analysis to find clusters of shared visions or perspectives of an issue by looking for individual patterns in each Q-sort, and using the analytical principle of correlation between individuals to find engagement or disengagement on a statement (Zabala 2014). The analysis reduces the perspectives in factors, a set of new parameters that represent an idealized Q-sort that summarizes the perspectives of the group (Webler et al. 2009). The number of factors depends on the number of Q-statements and Q-sorts, ideally the study must have a 3:1 ratio, respectively. In our case, the numbers did not match the suggested ratio, however, the Q-methodology researchers agreed to have a tolerance for the number of Q-statements and Q-sorts (Webler et al. 2009). For our analysis, we used 4 factors whose configurations of statements were later interpreted as meta-narratives.

References:
-	R Core Team (2020). R: A language and environment for statistical computing. R Foundation for Statistical Computing, Vienna, Austria. https://www.R-project.org/ 
-	Webler T, Danielson S, Tuler S (2009) Using Q Method to Reveal Social Perspectives in Environmental Research. Soc Environ Res 01301:1–54
-	Zabala A (2014) qmethod: A Package to Explore Human Perspectives Using Q Methodology. R J 6:163–173

## Results annex

### Results of Q-Methodology T0

Arguments for the statistical Q-analysis T0: 28 statements, 15 Q-sorts, “FALSE” forced distribution, 4 factors, varimax rotation, automatic flagging and Pearson correlation coefficient.

_Table 1. Q-sort factor loadings for Q-methodology T0_
_Factor loadings for Q-sorts indicates the relationship between each Q-sort and component or factor. Factors result in the meta-narratives described below. Italic numbers (>0.5) are the Q-sorts (rows) associated with that factor (columns)._

|Participants	 |Factor 1	 |Factor 2	 |Factor 3	 |Factor 4  |
|---------------|-------|-------|-------|------|
|Ac-01 	|_0.789_	|0.226	|0.400	 |0.178 |
|Ch-02 	|_0.544_	|0.463	|0.095	 |-0.167|
|Ngo-04 |0.196	|0.242	|_0.715_	 |-0.015|
|Cs-05	 |0.268	|0.243	|0.016	 |_0.797_ |
|Ac-06	 |0.247	|_0.677_	|0.132	 |0.231 |
|Ch-07 	|_0.741_	|0.303	|0.223	 |0.055 |
|Co-08 	|0.177	|_0.852_	|0.254	 |0.101 |
|Ch-09 	|_0.723_	|0.182	|-0.398 |0.257 |
|Ch-10 	|_0.707_	|0.299	|0.296	 |0.278 |
|Cs-14	 |0.012	|0.049	|_0.782_	 |0.408 |
|Gov-15 |0.374	|_0.700_	|0.232	 |0.442 |
|Cs-16 	|_0.757_	|0.125	|0.308	 |0.298 |
|Cs-17 	|0.207	|0.255	|_0.758_	 |-0.179|
|Ngo-18 |_0.749_	|0.086	|-0.022	|0.483 |
|Ac-19 	|_0.705_	|0.506	|0.121	 |-0.131|

_Figure 1. Q-methodology T0 plot. Statements comparing Z-scores by the 4 factors._
_Statements with largest consensus (bottom): 1, 5, 11, 24, 21, 3 and 26. Z-score values that distinguish a given statement and factor are represented with a filled symbol._
 
 <img src="Rplot_4factors_15part.png">



(Developed by Patricia Pérez-Belmont)
