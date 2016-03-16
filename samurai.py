import os
import subprocess
import re
from colour import Color
import json

sourceDir = "source_videos"

def generateThumbs():
#for all source videos, make thumbnail folder and populate it with thumbnails
  for vid in os.listdir(sourceDir):
    fileParts = re.search('Samurai\.Jack\.S(\d*)E(\d*)\.(\w*)\.(.*)\.avi', vid)
    season = fileParts.group(1)
    episode = fileParts.group(2)
    chapter = fileParts.group(3)
    title = fileParts.group(4).replace("."," ")

    folder = "S%sE%s"%(season, episode)

    print season, episode, chapter, title

    try:
      os.mkdir("thumbs/%s"%folder)
    except OSError:
      pass
#-ss 78 starts at second 78 (skips the credits, since they would contribute the same pixels to every map)
#fps=1 means a screenshot every second
    subprocess.call(['ffmpeg','-i', '%s/%s'%(sourceDir,vid), '-ss','78', '-vf', 'fps=1','thumbs/%s/thumb-%%d.png'%folder])

def generateHists():
#Generates a histogram of the twenty most common colors for every thumbnail
  with open('output.json', 'w') as fp:
    subprocess.call(['echo','{'], stdout=fp)
    for folder in os.listdir("thumbs"):
      print folder
      if(folder == '.DS_Store'):
        continue
      with open('data/%s.txt'%folder, 'w') as hist:
        for file in os.listdir('thumbs/%s'%folder):
          if(folder == '.DS_Store'):
            continue
#write color histogram to a temporary file
          subprocess.call(['convert', 'thumbs/%s/%s'%(folder, file), '-format', '%c', '-depth', '8',  'histogram:info:histogram_image.txt'])
#pipe that file to sort
          p1 = subprocess.Popen(['sort', '-n', 'histogram_image.txt'], stdout=subprocess.PIPE)
#write the 20 most common colors, for each thumbnail, to a text file
          subprocess.Popen(["tail", "-20"], stdin=p1.stdout, stdout=hist)
          p1.stdout.close()


def generateMaps():
#Builds to final images!
  for file in os.listdir('data'):
    if(file == '.DS_Store'):
      continue
    with open('data/%s'%file) as f:
      lines = f.readlines()
      for i, s in enumerate(lines):
#grab the hex color from each line of the histogram, convert to a color object
        hexGroups = re.search('(#.*) ', lines[i])
        hexColor = hexGroups.group(1)
        c = Color(hexColor)
        lines[i] = c.hsl
    colors = lines
#sort all colors by saturation, then divide into columns of length 100.
#Columns will be stacked left to right, meaning saturation will decrease left to right
    colors.sort(key=lambda tup: tup[1], reverse=True)
    chunk = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    colors = chunk(colors, 100)

#Then, within each column, sort first by value (lightest at top, darkest at bottom)
#then by hue, to sorta-kinda lump like-hues together, but make a nice mosaic effect
    for column in colors:
      column.sort(key=lambda tup: (tup[2],  tup[0]), reverse=True)

#Convert back to hex
    for column in colors:
      column[0:] = [Color(hsl=c).hex for c in column[0:]]
      
    h = len(colors)
    w = len(colors[0])
    with open('text/%s'%file, 'w') as f:
#write a .txt file which Imagemagick can convert to a png (a pixel map)
#Specify the dimensions and color space (1 color gets a 3x3 square of pixels, for sharper images)
      f.write("# ImageMagick pixel enumeration: %i,%i,255,srgb\n"%(h*3,w*3))
      for r in range(0, h):
        for c in range(0, w):
          for i in range(0, 9):
            R = r*3
            C = c*3
#The 3x3 blocks, per pixel. Note rows and columns are reversed, to rotate the image
            tups = [(R, C),(R,C+1),(R,C+2),(R+1,C),(R+1,C+1),(R+1,C+2),(R+2,C),(R+2,C+1),(R+2,C+2)]
            try:
#Write each color line
              col = colors[r][c]
              f.write("%i,%i: "%tups[i])
              rgb = Color(col).rgb
              new = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
              f.write("%s  "%str(new))
              f.write(col)
              f.write("  srgb%s"%str(new))
              f.write("\n")
            except IndexError:
#Pixel maps aren't perfect rectangles, so break on index error
              break
#Convert .txt file to .png
    subprocess.call(["convert", "text/%s"%file, "img/%s"%file.replace(".txt",".png")])

def buildHTML():
#For the html, convert file names to labels
  with open('index.txt', 'w') as f:
    for vid in os.listdir(sourceDir):
      fileParts = re.search('Samurai\.Jack\.S(\d*)E(\d*)\.(\w*)\.(.*)\.avi', vid)
      season = fileParts.group(1)
      episode = fileParts.group(2)
      chapter = fileParts.group(3)
      title = fileParts.group(4).replace("."," ")

      folder = "S%sE%s"%(season, episode)
#Doesn't build index.html, just did some regex-group find+replace in Sublime to generate html from index.txt
      f.write('%s::%s::Season %i, Episode %i\n'%(folder, title, int(season), int(episode)))


generateThumbs()
generateHists()
generateMaps()
buildHTML()




