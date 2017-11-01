command = "python ../fobject/manage.py"

subcommands = [
    'load_sectors',   #  egonet_type
    'load_alter_edges',  #  egonet

    'load_mental_items',  #  mm types
    'load_mental_edges',  #  mm
    
    'load_action_edges', # agency
]




suffix = {
    'load_action_edges': "agencynet.csv",
    'load_alter_edges': "egonet.csv",
    'load_mental_edges': "mm.csv",
    'load_mental_items': "mm_type.csv",
    'load_sectors': "egonet_type.csv"}

keys = [
    '001',
    '002',
    '006',
    '007',
    '009',
    '012',
    '015',
    '016',
    '017' ]

for sc in subcommands:
    for k in keys:
        print "%s %s joined/TL%s_%s" % (command, sc, k, suffix[sc])
