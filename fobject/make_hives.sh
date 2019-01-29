#!/bin/bash

python hiveplot_actioncats_joined.py --phase 'baseline'
python hiveplot_actioncats_joined.py --phase 'post-earthquake'
python hiveplot_actioncats_joined.py --phase 'phase 3'

python hiveplot_actioncats_joined.py --phase 'baseline' --egos TL010 TL016 TL014
python hiveplot_actioncats_joined.py --phase 'post-earthquake' --egos TL010 TL016 TL014
python hiveplot_actioncats_joined.py --phase 'phase-3' --egos TL010 TL016 TL014

find . -iname 'ana_hiveplot*svg' -printf "inkscape -D -e \`basename %p .svg\`.png %p \n" | sh
