#!/usr/bin/env python

import sys
import csv
import feedparser as parser
import threading
import Queue
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

N_THREADS = 10
TIMEOUT = 1
jobs = Queue.Queue(0)
rss_queue = Queue.Queue(N_THREADS)


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


def thread():
    """
    Defines the behavior of each thread in the Queue.
    The threads get tuples from the main queue and
    put it into the RSS queue for processing.
    """
    while True:
        try:
            feed_id, feed_url = jobs.get(False)  # Do not wait
        except Queue.Empty:
            return
        rss_queue.put((feed_id, feed_url), True)  # Block if full


@timeit
def run():
    """
    Main function that fills the queues, processes the threads,
    and writes the non-redundant feeds to an output file.
    """
    with open(in_file) as in_tsv:
        tsvreader = csv.reader(in_tsv, delimiter="\t")
        # skip header
        next(tsvreader, None)
        for line in tsvreader:
            feed_id = line[0]
            feed_url = line[1]
            # Fill the main queue
            jobs.put([feed_id, feed_url])

    # Start concurrency
    for x in range(N_THREADS):
        t = threading.Thread(target=thread)
        t.start()

    # Evaluate feeds and write to external file
    with open(out_file, "w") as out_tsv:
        out_tsv.write("#Feed ID\tURL\n")
        while threading.active_count() > 1 or not rss_queue.empty():
            try:
                feed_id, feed_url = rss_queue.get(False, TIMEOUT)
            except Queue.Empty:
                continue
            links = getLinks(feed_url)
            if links:  # not empty set
                out_tsv.write(feed_id + "\t" + feed_url + "\n")
                print("Feed with ID " + feed_id + " not redundant.")
            else:
                print("Feed with ID " + feed_id + " redundant. Deduplicated.")

    print("... RSS Parsing Completed")


run()
