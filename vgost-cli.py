#!/usr/bin/env python
import os, re, requests, sys, urllib

if len(sys.argv) > 1:
    write_location = " ".join(sys.argv[1:])
else:
    write_location = ""

site_url = "https://downloads.khinsider.com"
albumarr = []

while(len(albumarr) == 0):
    gamename = input("Enter search query: ").replace(" ", "+")
    searchpage = requests.get(site_url + "/search?search=" + gamename)
    albumarr = re.findall(r"<a href=\"/game-soundtracks/album.*</a>", searchpage.text)
    if(len(albumarr) == 0):
        print("No search results found!")

if searchpage.history and searchpage.url != searchpage.history[0].url:
    #redirect detected, no need to choose an album
    pagetitle = searchpage.text[searchpage.text.find('<title>') + 7 : searchpage.text.find('</title>')]
    foldername = re.findall(r".*MP3 - Download ", pagetitle)[0][:-16]
    albumpage = searchpage
else:
    albumlinklib = {}
    for x, album in enumerate(albumarr):
        albumlinklib[x + 1] = [album[album.find("\">")+2:-4], site_url + album[9:album.find("\">")]]

    for key in albumlinklib:
        print("[{}] {}".format(key, albumlinklib[key][0]))

    gameentry = int(input("Enter selection number: "))
    foldername = albumlinklib[gameentry][0]
    albumpage = requests.get(albumlinklib[int(gameentry)][1])

songarr = re.findall(r"<a href=\"/game-soundtracks/album.*mp3\">[^<]*</a>", albumpage.text)

songlinklib = {}
for x, song in enumerate(songarr):
    songlinklib[x + 1] = [song[song.find("\">")+2:-4], site_url + song[9:song.find("\">")]]

os.mkdir(write_location + "/" +foldername)

for key in songlinklib:
    title = "({}) - {}.mp3".format(key, songlinklib[key][0])
    link = songlinklib[key][1]
    print("Now downloading " + title)
    dllink = re.findall(r"https://.*com/.*mp3", requests.get(link).text)
    with open(write_location + "/" + foldername + "/" + title, "wb") as f:
        with urllib.request.urlopen(dllink[0]) as r:
            f.write(r.read())
