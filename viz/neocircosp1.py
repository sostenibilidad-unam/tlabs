import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go



def stats(g):
    K=np.array([k[1] for k in nx.degree(g)])    
    return {'nodes': len(g.nodes),
            'edges': len(g.edges),
            'density': nx.density(g),
            'avg. number of neighbors': K.mean()}




g = nx.DiGraph()

g.add_edge('Ngo-18', 'Outreach_tours_and_events')
g.add_edge('Ch-02', 'Outreach_tours_and_events')
g.add_edge('Ngo-18', 'Capacity_building_sustainable_agricultural_techniques')
g.add_edge('Ch-02', 'Capacity_building_sustainable_agricultural_techniques')
g.add_edge('Ngo-18', 'Capacity_building_sustainable_management_of_chinampas')
g.add_edge('Ch-07', 'Capacity_building_sustainable_management_of_chinampas')
g.add_edge('Ngo-18', 'Capacity_building_economic_tools_for_projects')
g.add_edge('Ch-10', 'Capacity_building_economic_tools_for_projects')
g.add_edge('Ngo-18', 'Outreach_tours_and_events')
g.add_edge('Ch-10', 'Outreach_tours_and_events')
g.add_edge('Ngo-18', 'Research_water_quality')
g.add_edge('Ac-01', 'Research_water_quality')
g.add_edge('Ngo-18', 'Capacity_building_sustainable_management_of_chinampas')
g.add_edge('Ac-01', 'Capacity_building_sustainable_management_of_chinampas')
g.add_edge('Ngo-18', 'Outreach_chinampas_products_and_social_projects')
g.add_edge('Ac-01', 'Outreach_chinampas_products_and_social_projects')
g.add_edge('Ngo-18', 'Outreach_chinampas_projects')
g.add_edge('Gov-15', 'Outreach_chinampas_projects')
g.add_edge('Ngo-18', 'Project_restoration_and_chinampas_refugees')
g.add_edge('Cs-05', 'Project_restoration_and_chinampas_refugees')
g.add_edge('Cs-05', 'Project_restoration_and_chinampas_refugees')
g.add_edge('Cs-17', 'Project_restoration_and_chinampas_refugees')
g.add_edge('Ngo-18', 'Research_water_quality')
g.add_edge('Ac-19', 'Research_water_quality')
g.add_edge('Ac-19', 'Research_water_quality')
g.add_edge('Ac-01','Research_water_quality')

df = nx.to_pandas_adjacency(g)
df.to_csv('t0_nx.csv')



h = nx.DiGraph()

h.add_edge('Ngo-18', 'Outreach_tours_and_events')
h.add_edge('Ch-02', 'Outreach_tours_and_events')
h.add_edge('Ngo-18', 'Capacity_building_sustainable_agricultural_techniques')
h.add_edge('Ch-02', 'Capacity_building_sustainable_agricultural_techniques')
h.add_edge('Ngo-18', 'Capacity_building_sustainable_management_of_chinampas')
h.add_edge('Ch-07', 'Capacity_building_sustainable_management_of_chinampas')
h.add_edge('Ngo-18', 'Capacity_building_economic_tools_for_projects')
h.add_edge('Ch-10', 'Capacity_building_economic_tools_for_projects')
h.add_edge('Ngo-18', 'Outreach_tours_and_events')
h.add_edge('Ch-10', 'Outreach_tours_and_events')
h.add_edge('Ngo-18', 'Capacity_building_sustainable_management_of_chinampas')
h.add_edge('Ac-01', 'Capacity_building_sustainable_management_of_chinampas')
h.add_edge('Ngo-18', 'Outreach_chinampas_products_and_social_projects')
h.add_edge('Ac-01', 'Outreach_chinampas_products_and_social_projects')
h.add_edge('Ngo-18', 'Outreach_chinampas_projects')
h.add_edge('Gov-15', 'Outreach_chinampas_projects')
h.add_edge('Ngo-18', 'Project_restoration_and_chinampas_refugees')
h.add_edge('Cs-05', 'Project_restoration_and_chinampas_refugees')
h.add_edge('Cs-05', 'Project_restoration_and_chinampas_refugees')
h.add_edge('Cs-17', 'Project_restoration_and_chinampas_refugees')
h.add_edge('Ngo-18', 'Research_water_quality')
h.add_edge('Ac-19', 'Research_water_quality')
h.add_edge('Ngo-18', 'Capacity_building_reforestation')
h.add_edge('Ch-07', 'Capacity_building_reforestation')
h.add_edge('Cs-16', 'Project_rainwater_harvesting_systems')
h.add_edge('Ngo-04', 'Project_rainwater_harvesting_systems')
h.add_edge('Cs-16', 'Alliance_farmers_market_certification')
h.add_edge('Ch-10', 'Alliance_farmers_market_certification')
h.add_edge('Cs-16', 'Alliance_advise_on_irregular_settlements_involvement')
h.add_edge('Ch-14', 'Alliance_advise_on_irregular_settlements_involvement')

df = nx.to_pandas_adjacency(h)
df.to_csv('t1_nx.csv')


gdf=pd.DataFrame.from_records([nx.out_degree_centrality(g),
                               nx.out_degree_centrality(h)])
gdf.to_csv('out_degree_centrality.csv')


df = pd.DataFrame.from_records([stats(g),
                                stats(h)])



fig = go.Figure(data=go.Parcoords(line=dict(color=df.index,
                                            colorscale=[[0,'#6e71a8'],
                                                        [1,'#cc544e']]),
                                  dimensions=list([
                                      dict(range = [0,30],
                                           label = 'nodes', values = df['nodes']),
                                      dict(range = [0,30],
                                           label = 'edges', values = df['edges']),
                                      dict(range = [0,1],
                                           label = 'density', values = df['density']),
                                      dict(range = [2,2.5],
                                           label = 'avg. neighbors', values = df['avg. number of neighbors'])])))

                #               , color="species_id", labels={"species_id": "Species",
                # "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                # "petal_width": "Petal Width", "petal_length": "Petal Length", },
                #              color_continuous_scale=px.colors.diverging.Tealrose,
                #              color_continuous_midpoint=2)
fig.show()









