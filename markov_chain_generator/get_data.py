import re
import time
import json
import requests

from bs4 import BeautifulSoup


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

main_urls = [
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=25",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=50",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=75",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=100",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=125",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=150",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=175",
]

def get_html(urls):
    global headers
    season_html = {"1": {}, "2": {}, "3": {}, "4": {}, "5": {}, "6": {}, "7": {}, "8": {}, "9": {}}
    for url in urls:
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")
        links = soup.find_all("a")
        for link in links:
            if match := re.match(r"(\d{2})x(\d{2})(\/\d{2})? - (.*)", link.text):
                season_number = match.group(1)
                episode_numbers = [match.group(2)] if match.group(3) is None else [match.group(2), match.group(3)[1:]]
                episode_title = match.group(4)
                season_html[season_number][episode_numbers[0]] = {
                    "title": episode_title,
                    "url": "https://transcripts.foreverdreaming.org" + link["href"][1:],
                }
        time.sleep(0.2)
    return season_html

"""
with open("seasons.json", "w") as file:
    json.dump(get_html(main_urls), file, indent=4)
"""

def get_transcript(url):
    global headers
    transcript = []
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    main_div = soup.find("div", {"class": "postbody"})
    for p in main_div.find_all("p"):
        if character := p.find("strong", recursive=False):
            name = character.text
            text = p.text.replace(f"{name}:", "").strip()
            transcript.append((name, text))
    return transcript


with open("seasons.json", "r") as file:
    seasons = json.load(file)

"""
# Retrieve episode transcripts
for season,episodes in seasons.items():
    print(season)
    for episode,data in episodes.items():
        transcript = get_transcript(data["url"])
        seasons[season][episode]["transcript"] = transcript
        with open("seasons.json", "w") as file:
            json.dump(seasons, file, indent=4)
        time.sleep(0.2)
"""

# Build characters dictionary
characters = {}
for season,episodes in seasons.items():
    for episode,data in episodes.items():
        for name,line in data["transcript"]:
            if name not in characters:
                if not name.startswith("["):
                    name = name.replace(":", "").rstrip(".")
                    name = name.strip()
                    characters[name] = []
                else:
                    continue
            characters[name].append(line)

with open("characters.json", "w") as file:
    json.dump(characters, file, indent=4)