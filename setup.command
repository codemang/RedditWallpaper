#!/usr/bin/env python

import os

# Add new cron job to load new images every night at 8:00 PM
os.system("crontab -l > mycron")
os.system("echo '0 * * * * python ~/.RedditWallpaper/grabImages.py' >> mycron")
os.system("#install new cron file")
os.system("crontab mycron");
os.system("rm mycron")

# Create directory in home directory to house cronjob code and images
os.system("mkdir ~/.RedditWallpaper");
os.system("mkdir ~/Desktop/RedditWallpaper");
os.system("cp ~/Downloads/RedditWallpaper/src/* ~/.RedditWallpaper");

# Load new images right away to initially populate the images directory
os.system("python ~/.RedditWallpaper/grabImages.py");
