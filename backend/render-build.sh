#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render


echo "...Downloading Chrome"
mkdir -p $STORAGE_DIR/chrome
cd $STORAGE_DIR/chrome
wget -P ./ https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb
dpkg -x ./google-chrome-stable_114.0.5735.90-1_amd64.deb $STORAGE_DIR/chrome
rm ./google-chrome-stable_114.0.5735.90-1_amd64.deb
cd $HOME/project/src # Make sure we return to where we were

# be sure to add Chromes location to the PATH as part of your Start Command
# export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"

# add your own build commands...