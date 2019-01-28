#!/bin/bash

python hiveplot_actioncats_joined.py all 'baseline'
python hiveplot_actioncats_joined.py all 'phase 3'

inkscape -D -e  agency_actioncats_joined_baseline.png agency_actioncats_joined_baseline.svg
inkscape -D -e  agency_actioncats_joined_phase3.png agency_actioncats_joined_phase\ 3.svg
