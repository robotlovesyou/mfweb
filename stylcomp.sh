#!/bin/bash
echo Enabling Node 0.8
~/.nvm/nvm.sh use 0.8
echo Starting stylus compilation
stylus -w -o gigs/static/gigs/stylesheets/ gigs/styl/styles.styl