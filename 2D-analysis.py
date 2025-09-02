import anastruct as anas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cowsay

ss = anas.SystemElements()

# Load up data
data_path = '2D-analysis.xlsx'
nodes = pd.read_excel(data_path,sheet_name='Nodes',index_col='id')
sections = pd.read_excel(data_path,sheet_name='Sections',index_col='name')
elements = pd.read_excel(data_path,sheet_name='Elements',index_col='id')
supports = pd.read_excel(data_path,sheet_name='Supports')
loads = pd.read_excel(data_path,sheet_name='Loads')

# Populate the model
for idx, d in elements.iterrows():
    spring={}
    if not np.isnan(d['fix1']): spring.update({1:d['fix1']}) 
    if not np.isnan(d['fix2']): spring.update({2:d['fix2']}) 
    ss.add_element(location=[[nodes.loc[d['node1'],'x'],nodes.loc[d['node1'],'y']],[nodes.loc[d['node2'],'x'],nodes.loc[d['node2'],'y']]],EA = sections.loc[d['section'],'E']*sections.loc[d['section'],'A'],EI=sections.loc[d['section'],'E']*sections.loc[d['section'],'I'],spring=spring)

for idx, d in supports.iterrows():
    if d['type'] == 'pin':
        ss.add_support_hinged(node_id=d['node'])
    if d['type'] == 'roller':
        ss.add_support_roll(node_id=d['node'])
    if d['type'] == 'fixed':
        ss.add_support_fixed(node_id=d['node'])
    if d['type'] == 'spring':
        ss.add_support_spring(node_id=d['node'],k=d['k'],translation=d['spring type'],roll=False)        


for idx,d in loads.iterrows():
    if d['type'] == 'q':
        ss.q_load(q=d['load'], element_id=d['id'], direction=d['direction']) 
    if d['type'] == 'M':
        ss.moment_load(node_id=d['id'],Ty=d['load'])
    if d['type'] == 'F':
        ss.point_load(node_id=d['id'],Fy=d['load'],rotation=d['direction'])

# Plotting
fig = ss.show_structure(show=False)
plt.savefig(fname='Arrangement.svg')
ss.solve()

fig = ss.show_axial_force(show=False)
plt.savefig(fname='Axial Force.svg')
fig = ss.show_shear_force(show=False)
plt.savefig(fname='Shear Force.svg')
fig = ss.show_bending_moment(show=False)
plt.savefig(fname='Bending Moment.svg')
fig = ss.show_displacement(show=False)
plt.savefig(fname='Displacement.svg')
fig = ss.show_reaction_force(show=False)
plt.savefig(fname='Reactions.svg')

# Tables
element_results = pd.DataFrame(ss.get_element_results(element_id=0,verbose=False))
node_results = pd.DataFrame(ss.get_node_results_system(node_id=0))

with pd.ExcelWriter('2D-results.xlsx') as writer: 
    element_results.to_excel(writer,sheet_name='Elements')
    node_results.to_excel(writer,sheet_name='Nodes')

# Complete
cowsay.cow('Successful moooooodelling!')