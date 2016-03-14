import os
import subprocess
import re

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

generateHist()