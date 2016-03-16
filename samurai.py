import os
import subprocess
import re
from colour import Color
import json

sourceDir = "source_videos"

def generateThumbs():
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

    subprocess.call(['ffmpeg','-i', '%s/%s'%(sourceDir,vid), '-ss','78', '-vf', 'fps=1','thumbs/%s/thumb-%%d.png'%folder])

def generateHist():
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
          subprocess.call(['convert', 'thumbs/%s/%s'%(folder, file), '-format', '%c', '-depth', '8',  'histogram:info:histogram_image.txt'])
          p1 = subprocess.Popen(['sort', '-n', 'histogram_image.txt'], stdout=subprocess.PIPE)
          subprocess.Popen(["tail", "-20"], stdin=p1.stdout, stdout=hist)
          p1.stdout.close()


def cleanHist():
  for file in os.listdir('data'):
    if(file == '.DS_Store'):
      continue
    with open('data/%s'%file) as f:
      lines = f.readlines()
      for i, s in enumerate(lines):
        hexGroups = re.search('(#.*) ', lines[i])
        hexColor = hexGroups.group(1)
        c = Color(hexColor)
        lines[i] = c.hsl
    colors = lines
    colors.sort(key=lambda tup: tup[1], reverse=True  )

    chunk = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

    colors = chunk(colors, 100)

    for row in colors:
      row.sort(key=lambda tup: (tup[2],  tup[0]), reverse=True)

    for row in colors:
      row[0:] = [Color(hsl=c).hex for c in row[0:]]
      
    h = len(colors)
    w = len(colors[0])
    with open('text/%s'%file, 'w') as f:
      f.write("# ImageMagick pixel enumeration: %i,%i,255,srgb\n"%(h*3,w*3))
      for r in range(0, h):
        for c in range(0, w):
          for i in range(0, 9):
            R = r*3
            C = c*3
            tups = [(R, C),(R,C+1),(R,C+2),(R+1,C),(R+1,C+1),(R+1,C+2),(R+2,C),(R+2,C+1),(R+2,C+2)]
            try:
              col = colors[r][c]
              f.write("%i,%i: "%tups[i])
              rgb = Color(col).rgb
              new = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
              f.write("%s  "%str(new))
              f.write(col)
              f.write("  srgb%s"%str(new))
              f.write("\n")
            except IndexError:
              break
    subprocess.call(["convert", "text/%s"%file, "img/%s"%file.replace(".txt",".png")])

def buildHTML():
  for vid in os.listdir(sourceDir):
  fileParts = re.search('Samurai\.Jack\.S(\d*)E(\d*)\.(\w*)\.(.*)\.avi', vid)
  season = fileParts.group(1)
  episode = fileParts.group(2)
  chapter = fileParts.group(3)
  title = fileParts.group(4).replace("."," ")

  folder = "S%sE%s"%(season, episode)

  # print season, episode, chapter, title
  with open('index.txt', 'w') as f:
    f.write('%s::%s::Season %i, Episode %i\n'%(folder, title, season, episode))

buildHTML()
# generateThumbs()
# generateHist()
# cleanHist()





