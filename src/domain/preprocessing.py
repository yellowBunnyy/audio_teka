from bs4 import BeautifulSoup
import re

file = "audioteka_test.html"
everything = set()
with open(file) as f:
    soup = BeautifulSoup(f, "html.parser")
    l = soup.find_all("span")
    pattern = "(<span>)(.+)(span)"
    everything = set()
    for text in l:
        container = re.findall(pattern, str(text))
        position = list(set([c[1].strip("</span>") for c in container]))
        everything.add(position[0])

for title in sorted(everything):
    print(title)


