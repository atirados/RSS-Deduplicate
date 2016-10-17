#!/usr/bin/env python

import sys
import csv
import feedparser as parser
import argparse

""" RSS Parser that removes redundant URLs """

__author__ = "Adrian Tirados"
__email__ = "atirados@hawk.iit.edu"

"""
parser = argparse.ArgumentParser(
        description='This scripts optimizes a list of RSS feeds by removing duplicates')
parser.add_argument(
        '-f', '--file', help='TSV file containing the RSS feeds', required=True)
parser.add_argument(
        '-e', '--empty', help='How to treat empty RSS feeds. Options: keep/discard. ', required=True)
    args = parser.parse_args()

feed_file = args.file
empty = args.empty
"""
feed_file = "short_list.tsv"

all_links = set()
optimized_feeds = []

def getLinks(url):
	links = set()
	feed = parseRSS(url)
	for entry in feed.entries:
		if not entry.link in all_links:
			all_links.add(entry.link)
			links.add(entry.link)
	return links

def parseRSS(url):
    return parser.parse(url)

with open(feed_file) as tsvfile:
	tsvreader = csv.reader(tsvfile, delimiter="\t")
	# skip header
	next(tsvreader, None)
	for line in tsvreader:
		print(line)
		feed_url = line[1]
		links = getLinks(feed_url)
		if links: #not empty set
			optimized_feeds.append(line)
		print("Number of Unique Links: "+ str(len(all_links)))

print(len(optimized_feeds))