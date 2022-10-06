from bs4 import BeautifulSoup
import re

everything = set()


def find_title(texts):
    global everything
    for text in texts:
        everything.add(extract_title_from_string(str(text)))


def extract_title_from_string(string: str):
    pattern = "<span>|</span>"
    text = re.split(pattern, string)[1]
    if "<i>" in text:
        text = text.replace("<i>", "odcinek: ").strip("</i>")
    return text


def main():
    file = "audioteka_new.html"
    with open(file) as f:
        finded_tags = extract_text_using_tag(f)
        find_title(finded_tags)
    printAllTitles(everything)


def extract_text_using_tag(file, tag: str = "span"):
    soup = BeautifulSoup(file, "html.parser")
    finded_tags = soup.find_all(tag)
    tags_withou_repetitions = finded_tags[
        1::2
    ]  # start from first index and grap every second
    return tags_withou_repetitions


def printAllTitles(titles):
    for title in sorted(titles):
        print(title)
    print(len(titles))


if __name__ == "__main__":
    main()
