#!/usr/bin/python

#Scaping all MP3 files from the Gothic audio books at https://kg-voices.de
#Author(s)		: Lukas Mirow
#Date of creation	: 2023-09-01


DOWNLOADER_EXECUTABLE = "yt-dlp"
DOWNLOADER_FLAGS = "--abort-on-unavailable-fragments"
URL = "https://kg-voices.de/gothic-2-hoerspiel"
SEARCH_PATTERN = "https:\/\/kg-voices\.de\/wp-content\/uploads\/[a-z0-9\/-]+\.mp3"
EXCLUDE_PATTERN = "\/bald\.mp3\>"


import requests
import re
from os import system


def error(msg):
	print(f"Error: {msg}")
	exit(1)

if __name__ == "__main__":

	#Get page source
	req = requests.get(URL)
	if req.status_code != 200:
		error(f"An error occurred trying to download the source code of the website, url was `{URL}`")

	#Search for links to MP3 files
	links = []
	re_search = re.compile(SEARCH_PATTERN, re.IGNORECASE)
	re_exclude = re.compile(EXCLUDE_PATTERN, re.IGNORECASE)
	search_txt = req.text
	search_txt = req.text
	match = re_search.search(search_txt)
	while match != None: #For each match
		link = search_txt[match.start():match.end()]
		#Ignore the "will come soon"-MP3s
		if not re_exclude.fullmatch(link):
			#Ignore duplicates
			if link not in links:
				#Add to list of links
				links.append(link)
		print(f"\rCreating list of files to download...{len(links)}", end="")
		#Continue searching after the match
		search_txt = search_txt[match.end():]
		match = re_search.search(search_txt)
	print()

	#Download all files
	for i in range(len(links)):
		system(f"{DOWNLOADER_EXECUTABLE} {DOWNLOADER_FLAGS}  -o '{i:02d}.%(ext)s' '{links[i]}'")
