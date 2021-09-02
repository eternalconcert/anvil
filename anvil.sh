#!/bin/bash

python3 /etc/anvil/render_html.py $@
node /etc/anvil/render_styles.js $@
