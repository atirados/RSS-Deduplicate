#!/usr/bin/env python

import sys
import csv
import feedparser as parser

""" RSS Parser that removes redundant URLs """

__author__ = "Adrian Tirados"
__email__ = "atirados@hawk.iit.edu"

# Input and output files
in_file = sys.argv[1]
out_file = sys.argv[2]

# Global set of links
all_links = set()


def getLinks(url):
    """
    Returns all unique links from a RSS feed url
    """
    links = set()
    feed = parseRSS(url)
    for entry in feed.entries:
        entry_link = getattr(entry, 'title', '')
        if entry_link not in all_links:
            all_links.add(entry_link)
            links.add(entry_link)
    return links


def parseRSS(url):
    """
    Parses a RSS feed url to obtain all its parameters
    """
    return parser.parse(url)


with open(in_file) as in_tsv:
    with open(out_file, "w") as out_tsv:
        tsvreader = csv.reader(in_tsv, delimiter="\t")
        # skip header
        next(tsvreader, None)
        out_tsv.write("#Feed ID\tURL\n")
        print("Parsing RSS Feeds...")
        for line in tsvreader:
            feed_url = line[1]
            links = getLinks(feed_url)
            if links:  # not empty set
                out_tsv.write(line[0] + "\t" + line[1] + "\n")
                print("Feed with ID " + line[0] + " not redundant.")
            else:
                print("Feed with ID " + line[0] + " redundant. Deduplicated.")

print("... RSS Parsing Completed")
