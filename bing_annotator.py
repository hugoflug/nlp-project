import urllib.parse
import urllib.request
import re

#p = re.compile('<div class="b_title"><h2><a href="http://en.wikipedia.org/wiki/')
p = re.compile('<div class="b_title"><h2><a href="http://en.wikipedia.org/wiki/[^"]*"')

response = urllib.request.urlopen("http://www.bing.com/search?q=" + "Armstrong" + "+site%3Aen.wikipedia.org")
#output = response.decode('utf-8')

for (letters) in p.findall(response.read().decode('utf-8')):
    print(letters[63:-1])
    