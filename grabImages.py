import os
import re
import datetime

from datetime import timedelta
from os.path import expanduser


timeStructure = '%Y/%m/%d %H:%M:%S'     # Format for date/time
timeDiff = timedelta(hours=12)          # Amount of time to wait between updates
scheduleFile = '.RedditWallpaper/schedule.txt'         # File where last update time is stored

def main():
  
  global scheduleFile
  scheduleFile = expanduser("~") + "/" + scheduleFile

  # If nothing has been written to schedule.txt, this is the first time grabbing images 
  if os.stat(scheduleFile).st_size == 0:
    print "Empty"
    grabImages()
    return

  # Read the last time the images were updated
  f = open(scheduleFile, 'r')
  lastTimeUpdated = f.readline().rstrip('\n')

  # Grab the current time and strip the decimal place following the time
  curTime = datetime.datetime.now()
  curTime = curTime.strftime(timeStructure)
  curTime = datetime.datetime.strptime(curTime, timeStructure)

  # Convert lastTimeUpdated from a string to a datetime object
  lastTimeUpdated = datetime.datetime.strptime(lastTimeUpdated, timeStructure)

  # If it has been more than timeDiff hours since the last update, update
  if lastTimeUpdated + timeDiff < curTime:
    grabImages()
    return


def grabImages():
  # Grab entire HTML of r/EarthPorn
  os.system("curl www.reddit.com/r/EarthPorn > output.txt")

  # Load HTML of r/EarthPorn into variable 
  f = open('output.txt', 'r')
  body = f.read()

  thumbnailRegex = re.compile('<a class="thumbnail.+?href="(.+?)"')
  badImgurRegex = re.compile('^https?://(www.)?imgur.com/.+')
  goodImgurRegex = re.compile('^https?://i.imgur.com.*')
  ppcdnRegex = re.compile('^https?://ppcdn.500px.org.*')
  grabImgurRegex = '^https?://(www.)?(imgur.com/.+)'

  counter = 1

  # For every thumbnail image in the page
  for link in re.findall(thumbnailRegex, body):
    # If we have already downloaded 10 images, break
    if counter > 10:
      break;

    # If this thumbnail is not from imgur or ppcdn, try again
    if not goodImgurRegex.match(link) and not badImgurRegex.match(link) and not ppcdnRegex.match(link):
      continue;

    if badImgurRegex.match(link):
      m = re.search(grabImgurRegex, link)
      link = "i." + m.group(2)+".jpg"


    # Create an image name for this image and download the image
    imageName = "image"+`counter`+".jpg"
    command = 'curl -o '+imageName +' '+link + ' > /dev/null'
    os.system(command)

    # Move the image to the images directory
    os.system("mv "+imageName+" ~/Desktop/RedditWallpaper/"+imageName)
    counter += 1

  
  curTime = datetime.datetime.now()
  curTime = curTime.strftime(timeStructure)
  f = open(scheduleFile, 'w')
  f.write(curTime)

  os.system("rm ./output.txt")

if __name__ == "__main__":
  main()
  
