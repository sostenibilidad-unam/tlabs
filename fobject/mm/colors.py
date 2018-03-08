def sector_color(alter):
    sector_color = {'Academia': 'blue',
                    'Gobierno': 'green',
                    None: 'orange',
                    'Ego': 'tomato',
                    'Otros': 'purple',
                    'Privado': 'purple',
                    'Sociedad_Civil': 'gold'}
    if alter.sector:
        sector = alter.sector.name
    else:
        sector = None

    return sector_color[sector]


def practice_color(action):
    practice_color = {
        'Research': 'darkcyan',
        'Training': 'firebrick',
        'Agricultural/ecological training': 'orange',
        'Outreach': 'green',
        'Market': 'blue',
        'Education': 'teal',
        'Funding': 'grey',
        'Collaboration': 'red',
        'Financial/commercial training': 'yellow',
        'Social organization': 'cornflowerblue',
        'Tourism': 'forestgreen',
        'Management': 'dodgerblue',
        'Networking': 'goldenrod',
        'Production': 'midnightblue',
        'Construction': 'darkgreen',
        'Culture': 'cyan',
        'Consultancy': 'hotpink',
        'Ecological conservation': 'lightcoral',
        'Citizen assistance': 'indigo',
        'Legal training': 'brown',
    }
    if action.category:
        return practice_color[action.category.name]
    else:
        return "purple"
