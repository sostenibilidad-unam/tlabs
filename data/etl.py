command = "python ../fobject/manage.py"

subcommands = [
    'load_sectors',  # egonet_type
    'load_alter_edges',  # egonet
    'load_action_edges',  # agency
    # 'load_mental_items',  #  mm types
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
    '017']

keys = ["%03i" % n for n in range(1, 19)]

keys.pop(12)
keys.pop(10)
keys.pop(2)

for sc in subcommands:
    for k in keys:
        print "ls v5/TL%s_%s" % (k, suffix[sc])
        print "%s %s v5/TL%s_%s" % (command, sc, k, suffix[sc])


print "%s load_ego_types ego_types.csv" % command

# for k in keys:
#     print "%s load_mental_edges --ego TL%s --csv joined/TL%s_%s" % (command,
#                                                                   k, k,
#                                                                   suffix['load_mental_edges'])
