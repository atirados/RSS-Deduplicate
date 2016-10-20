#!/usr/bin/env python

import sys
import csv
import feedparser as parser
import time
import timeit
import functools

""" RSS Parser that removes redundant URLs """

__author__ = "Adrian Tirados"
__email__ = "atirados@hawk.iit.edu"

# Input and output files
in_file = sys.argv[1]
out_file = sys.argv[2]

# Global set of links
all_links = set()

# Feeds dictionary
feeds_list = {}


def timeit(func):
    """
    Times the execution time of a decorated function.
    """
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc


def getLinks(url):
    """
    Returns all unique links from a RSS feed url
    """
    links = set()
    print("Parsing feed " + url)
    feed = parseRSS(url)
    for entry in feed.entries:
        entry_link = getattr(entry, 'link', '')
        links.add(entry_link)
    print("... Completed")
    return links


def parseRSS(url):
    """
    Parses a RSS feed url to obtain all its parameters
    """
    return parser.parse(url)


@timeit
def run():
    with open(in_file) as in_tsv:
        tsvreader = csv.reader(in_tsv, delimiter="\t")
        # skip header
        next(tsvreader, None)
        for line in tsvreader:
            feed_id = line[0]
            feed_url = line[1]
            feed_info = (feed_id, feed_url)
            links_list = getLinks(feed_url)
            feeds_list[feed_info] = links_list
    sorted_dict = sorted(feeds_list.items(),
                         key=lambda x: len(x[1]), reverse=True)

    print("Analizing feeds...")
    for i in sorted_dict:
        write = False
        for k in i[1]:
            if k in all_links:
                continue
            else:
                write = True
                all_links.add(k)
        if write:
            print("FEED WITH ID " + i[0][0] + " NOT REDUNDANT")
        else:
            print("FEED WITH ID " + i[0][0] + " REDUNDANT")


run()
