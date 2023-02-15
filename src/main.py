import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import os


def save_novel_data(novel, data):
    file = open(novel + ".json", "w")
    file.write(json.dumps(data))


def load_novel_data(novel):
    file = open(novel, "r")
    return json.loads(file.read().replace("\n", ""))


def get_from_possibles(possibles, soup):
    res = None
    if "find_all" in possibles:
        for p in possibles.keys():
            if str(p).__contains__("class"):
                try:
                    res = soup.find_all(class_=possibles.get(p))
                except:
                    res = None
            elif str(p).__contains__("element"):
                try:
                    res = soup.find_all(possibles.get(p))
                except:
                    res = None
            elif str(p).__contains__("id"):
                try:
                    res = soup.find_all(id=possibles.get(p))
                except:
                    res = None
            if res is not None:
                return res
    else:
        for p in possibles.keys():
            if str(p).__contains__("class"):
                try:
                    res = soup.find(class_=possibles.get(p))
                except:
                    res = None
            elif str(p).__contains__("element"):
                try:
                    res = soup.find(possibles.get(p))
                except:
                    res = None
            elif str(p).__contains__("id"):
                try:
                    res = soup.find(id=possibles.get(p))
                except:
                    res = None
            if res is not None:
                return res
    return res


def get_text(page_url, settings):
    soup = BeautifulSoup(requests.get(page_url).content, "html.parser")
    chapter_title = get_from_possibles(settings.get("title_finder"), soup).text
    if chapter_title is None:
        print("Couldn't find a chapter title, using 'CHAPTER NAME' as replacement")
        chapter_title = "CHAPTER NAME"
    chapter_text = get_from_possibles(settings["text_finder"], soup)
    if chapter_text is None:
        print("Chapter text is none")
        chapter_text = ""
    next_chapter_url = get_from_possibles(settings["next_page_finder"], soup)
    try:
        next_chapter_url = next_chapter_url["href"]
    except:
        next_chapter_url = None
    return {
        "title": chapter_title,
        "text": chapter_text,
        "next_page": next_chapter_url,
    }


novel = input("Select the novel data to use: ")
conf = load_novel_data(novel + ".json")

novel_path = os.path.join("books", novel)

if os.path.exists(novel_path):
    os.chdir(novel_path)
else:
    os.mkdir(novel_path)
    os.chdir(novel_path)
base_url = conf.get("base_url")
next_paragraph = conf.get("last")
file_name = next_paragraph.split("/")[1]

chapters = conf.get("chapters_done")
if conf.get("last_write_to") is not None:
    file_name_chapter = conf.get("last_write_to")
else:
    file_name_chapter = novel

do_skip = conf.get("skip")
while 69:
    if chapters % 100 == 0:
        file_name_chapter = f"{file_name} {chapters}-{chapters+100}"
        conf["last_write_to"] = file_name_chapter
        os.chdir("..")
        os.chdir("..")
        save_novel_data(novel, conf)
        os.chdir(novel_path)
    try:
        data = get_text((base_url + next_paragraph), conf)
    except AttributeError as e:
        os.chdir("..")
        os.chdir("..")
        save_novel_data(novel, conf)
        print(e.with_traceback(None))
        exit(-1)
    if do_skip:
        print("skipping...")
        if data.get("next_page") is not None:
            next_paragraph = data.get("next_page")
            print(next_paragraph)
            data = get_text((base_url + next_paragraph), conf)
            do_skip = False
        else:
            print("No new chapters were added.")
            exit(0)

    print("\033c", end="")
    print(f"Writing '{data.get('title')}'...")
    conf["skip"] = False
    with open((file_name_chapter + ".md"), "a", encoding="utf8", errors="ignore") as f:
        f.write("\n### " + data.get('title') + "\n")
        for paragraph in data.get("text"):
            f.write(paragraph.text.strip() + "\n\n")
    conf["skip"] = True
    if data.get("next_page") is not None:
        conf["last"] = next_paragraph
        next_paragraph = data.get("next_page")
    else:
        conf["skip"] = True
        os.chdir("..")
        os.chdir("..")
        save_novel_data(novel, conf)
        exit(0)
    chapters += 1
    conf["chapters_done"] = chapters
    sleep(.4)
