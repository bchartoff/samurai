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
      os.mkdir(folder)
    except OSError:
      pass

    subprocess.call(['ffmpeg', '-i', '%s/%s'%(sourceDir,vid), '-vf', 'fps=1', '%s/thumb-%%d.png'%folder])

  # subprocess.call(['echo',chapter])

  # break
def generateHist():
  with open('output.json', 'w') as fp:
    # fp.write('{')
    subprocess.call(['echo','{'], stdout=fp)
    for folder in os.listdir("thumbs"):
    # convert image.jpg  -format %c -depth 8  histogram:info:histogram_image.txt
    # sort -n histogram_image.txt | tail -1
      if(folder == '.DS_Store'):
        continue
      with open('data/%s.txt'%folder, 'w') as hist:
        for file in os.listdir('thumbs/%s'%folder):
          if(folder == '.DS_Store'):
            continue
          # subprocess.call(['echo', file], stdout=hist)
          print folder, file
          subprocess.call(['convert', 'thumbs/%s/%s'%(folder, file), '-format', '%c', '-depth', '8',  'histogram:info:histogram_image.txt'])
          p1 = subprocess.Popen(['sort', '-n', 'histogram_image.txt'], stdout=subprocess.PIPE)
          subprocess.Popen(["tail", "-10"], stdin=p1.stdout, stdout=hist)
          p1.stdout.close()
          # subprocess.call(['rm','histogram_image.txt'])
      # subprocess.call(['echo', 'foo\\n', '>>', 'output.json'], stdout=fp)

# generateHist()

def cleanHist():
  for file in os.listdir('data'):
    if(file == '.DS_Store'):
      continue
    with open('data/%s'%file) as f:
      lines = f.readlines()
      # print lines
      for i, s in enumerate(lines):
        # line 
        hexGroups = re.search('(#.*) ', lines[i])
        hexColor = hexGroups.group(1)
        c = Color(hexColor)
        lines[i] = c.hsl
    # season = fileParts.group(1)

      # lines[0:] = [line + 1 for line in lines[0:]]
      # for line in lines:
    # return lines
    colors = lines
    colors.sort(key=lambda tup: tup[2])

    chunk = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

    colors = chunk(colors, 200)

    for row in colors:
      row.sort(key=lambda tup: tup[0])

    for row in colors:
      row[0:] = [Color(hsl=c).hex for c in row[0:]]
      
    # print colors
    h = len(colors)
    w = len(colors[0])
    with open('text/%s'%file, 'w') as f:
      # ImageMagick pixel enumeration: 640,480,255,srgb
      f.write("# ImageMagick pixel enumeration: %i,%i,255,srgb\n"%(w,h))
      for r in range(0, h):
        for c in range(0, w):
          # print "%i,%i"%(c,r)
          try:
            col = colors[r][c]
            f.write("%i,%i: "%(c,r))
            rgb = Color(col).rgb
            new = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            f.write("%s  "%str(new))
            f.write(col)
            f.write("  srgb%s"%str(new))
            f.write("\n")
          except IndexError:
            # print
            break
    subprocess.call(["convert", "text/%s"%file, "img/%s"%file.replace(".txt",".png")])
          # print colors[r][c]


      # f.write("var colors=")

      # json.dump(colors, f, ensure_ascii=False)

    # break

cleanHist()
# colors = temp
#   c = Color(color)




