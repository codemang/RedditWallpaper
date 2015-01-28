#!/bin/bash

rm RedditWallpaper.zip

mkdir src
cp grabImages.py src
cp setup.command src

zip -r RedditWallpaper.zip src readme.txt

rm -rf src
