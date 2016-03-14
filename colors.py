import random
from colour import Color
import json

r = lambda: random.randint(0,255)

#actual will be 600x88
colors = []
for i in range(0, 52800):
  color = '#%02X%02X%02X' % (r(),r(),r())
  c = Color(color)

  colors.append(c.hsl)

#sort by value divide into 22 groups instead of 88
colors.sort(key=lambda tup: tup[2])

chunk = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

colors = chunk(colors, 600)

for row in colors:
  row.sort(key=lambda tup: tup[0])

for row in colors:
  row[0:] = [Color(hsl=c).hex for c in row[0:]]
  
# print colors

with open('colors.js', 'w') as f:
  f.write("var colors=")
  json.dump(colors, f, ensure_ascii=False)

